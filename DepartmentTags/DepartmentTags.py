# encoding:utf-8
import chardet
import uniout
from Common.FileServer.FileServer import FileServer
from Common.DBServer.DBServer import DBServer
from Common.MailServer.MailServer import MailServer


class DepartmentTags(object):
    '''
    验证数据库中科室标签是否正确，参照对象为存储在txt文件的科室标签信息
    创建类对象需传入目标数据库信息
    '''

    def __init__(self, db):
        '''
        初始化文件服务和数据库服务
        :param db: "mysql,root/6tfc^YHN@10.0.127.14:3306/sodap_dev"
        '''
        self.file_server = FileServer()
        self.db_server = DBServer(db)

    def get_filedata(self, file, format):
        str_data = self.file_server.file_read(file, format)
        return str_data

    def list_filedata(self, file, format):
        list_data = self.file_server.file_readlines(file, format)
        return list_data

    def list_dbdata(self, db, sql):
        db_server = DBServer(db)
        list_data = db_server.listDataBySQL(sql)
        return list_data

    def decode_data(self, data, code_format):
        if isinstance(data, str):
            return data.decode(code_format)
        elif isinstance(data, list):
            return [element.decode(code_format) for element in data]
        else:
            print("*ERROR* decode data type can only be str,list!")

    def get_refrence_tags(self, file, open_format):
        # 获取TXT文件数据到列表中
        tags_data = self.list_filedata(file, open_format)
        # 将列表数据按需要的格式进行解码
        code_format = self.file_server.get_encode_format(file)
        tags_data = self.decode_data(tags_data, code_format)
        # 建立科室-标签字典
        dept_tags = {}
        for dept_tag in tags_data:
            dept_tag = dept_tag.replace("\n", "")  # 去除多余换行符
            dept_tag = dept_tag.replace("\r", "")
            dept_tag = dept_tag.replace(" ", "")
            dept_tags[dept_tag.split(":")[0]] = dept_tag.split(":")[1].split(",")
        return dept_tags

    def get_taginfo(self):
        '''
        标签信息：标签id，标签名称，标签类型，删除标志
        :return: 标签信息列表
        '''
        sql = "SELECT * FROM tags WHERE tag_name NOT IN ('A+','A','B') AND is_deleted=0"
        tags_info = self.db_server.listDataBySQL(sql)
        return tags_info

    def get_deptinfo(self):
        '''
        科室信息：科室id，科室名称，医院id，医院名称
        :return: 科室信息列表
        '''
        sql = "SELECT d.id,d.name,d.hospital_id,h.name FROM departments d,hospitals h WHERE d.is_deleted = 0 and d.hospital_id=h.id"
        depts_info = self.db_server.listDataBySQL(sql)
        # for i in range(10):
        #     print len(depts_info[i][3])
        #     print ("%-10d%-30s%-10d%-30s" %(depts_info[i][2],self.myAlign(depts_info[i][3],30),depts_info[i][0],depts_info[i][1]))
        return depts_info

    def myAlign(self,string,length=0):
        if length == 0:
            return string
        slen = len(string)
        re_str = string
        if isinstance(string,str):
            placeholder = " "
        else:
            placeholder = "  "
        while slen < length:
            re_str += placeholder
            slen += 1
        return re_str


    def get_dept_taginfo(self):
        '''
        科室标签信息：科室id，科室名称，标签名称，标签id
        :return: 科室标签列表
        '''
        sql = "SELECT department_id,tag_name,tag_id FROM departmert_tag WHERE tag_name not in ('A+','A','B') and is_grade=0 ORDER BY department_id"
        depttags_info = self.db_server.listDataBySQL(sql)
        return depttags_info

    def assertTagsOfDepartments(self, depts_info,depttags_info, ref_tags_info):
        '''
        检查数据库中科室标签与参考文件中科室标签是否一致
        :param depts_info: 科室列表[(科室id，科室名称，医院id，医院名称),...]
        :param depttags_info: 科室标签列表[(科室id，科室名称，标签名称，标签id),...]
        :param ref_tags_info: 参考科室标签字典{科室名称:[标签1,标签2,...],...}
        :return:结果信息msg，未到标签的科室列表untaged_depts，未检验的科室列表unchecked_depts，标签有误的科室列表wrongtag_depts
        '''
        msg = [[u"医院id", u"医院", u"科室id", u"科室", u"标签", u"参考标签", u"结果"]]
        untaged_depts = []
        unchecked_depts = []
        wrongtag_depts = []
        for dept in depts_info:
            dept_id = dept[0]
            dept_name = dept[1]
            list_dept_tags = [depttags_info[i][1] for i in range(len(depttags_info)) if depttags_info[i][0] == dept_id]
            list_dept_tags_ref = ref_tags_info.get(dept_name,[])

            if len(list_dept_tags) == 0:  #数据库中未给该科室打标签
                msg.append([str(dept[2]),
                            dept[3],
                            str(dept_id),
                            dept_name,
                            "**",
                            u",".join(list_dept_tags_ref),
                            u"未打标签"])
                untaged_depts.append(dept)
            if len(list_dept_tags_ref) == 0:  # 参照文件中不存在该科室的标签信息
                msg.append([str(dept[2]),
                            dept[3],
                            str(dept_id),
                            dept_name,
                            u",".join(list_dept_tags),
                            "**",
                            u"参考标签不存在"])
                unchecked_depts.append(dept)
            if len(list_dept_tags) > 0 and len(list_dept_tags_ref) > 0:  #将数据库中标签与参考文件中做比较
                missed_tags = [tag for tag in list_dept_tags_ref if tag not in list_dept_tags]  #漏打的标签
                wrong_tags = [tag for tag in list_dept_tags if tag not in list_dept_tags_ref]   #错误的标签
                if len(missed_tags) > 0:
                    msg.append([str(dept[2]),
                                dept[3],
                                str(dept_id),
                                dept_name,
                                u",".join(list_dept_tags),
                                u",".join(list_dept_tags_ref),
                                u"不完整标签"])
                    wrongtag_depts.append(dept)

                if len(wrong_tags) > 0:
                    msg.append([str(dept[2]),
                                dept[3],
                                str(dept_id),
                                dept_name,
                                u",".join(list_dept_tags),
                                u",".join(list_dept_tags_ref),
                                u"错误标签"])
                    wrongtag_depts.append(dept)
        return msg,untaged_depts,unchecked_depts,wrongtag_depts

    def attachTagsToDept(self,depts_info,tags_info,ref_tags_info):
        '''
        给科室打标签
        :param depts_info: 科室列表[(科室id，科室名称，医院id，医院名称),...]
        :param tags_info: 标签列表[(标签id，标签名称，标签类型，删除标志),...]
        :param ref_tags_info: 参考科室标签字典{科室名称:[标签1,标签2,...],...}
        :return:
        '''
        fail_taged_depts = []
        error_msg=[]
        sql_del = []
        sql_insert = []
        for dept in depts_info:
            # 获取参考标签名称列表
            tags = ref_tags_info.get(dept[1])
            if tags == None: #参考文件中没有该科室的标签信息
                fail_taged_depts.append(dept)
                error_msg.append("No tags for department in refrence file: %s" % str(dept))
                continue

            # 获取数据库中标签列表[(科室id，科室名称，标签id，标签名称),...]，根据标签名称获取标签id
            dept_tags_info = [(dept[0], dept[1], tags_info[i][0], tags_info[i][1])
                              for i in range(len(tags_info)) if tags_info[i][1] in tags]
            if len(dept_tags_info) == 0: #在数据库中未找到标签名称对应的标签信息
                fail_taged_depts.append(dept)
                error_msg.append("No tags for department in db-table(tags): %s\nTags(%s) must exsisted in dbtable(Tags)" % (str(dept),str(tags)))
                continue

            # 检查数据库中是否存在该科室的标签信息，有则先删除，然后再插入
            print "11111"
            sql_check = "SELECT * FROM departmert_tag WHERE department_id = %d " \
                        "AND tag_name NOT IN ('A+','A','B') AND is_grade=0" % (dept[0])
            if len(self.db_server.listDataBySQL(sql_check)) > 0:
                sql = "DELETE FROM departmert_tag WHERE department_id = %d " \
                      "AND tag_name NOT IN ('A+','A','B') AND is_grade=0" % (dept[0])
                sql_del.append(sql)
            for info in dept_tags_info:
                sql = "INSERT INTO departmert_tag(department_id,department_name,tag_id,tag_name,is_grade) " \
                      "VALUES ( %d,'%s',%d,'%s',0)" % (info[0], info[1].encode("utf-8"), info[2], info[3].encode("utf-8"))
                sql_insert.append(sql)
        if len(error_msg)>0:
            print(u"*ERROR* 以下科室标签更新失败")
            print("\n".join(error_msg))
        # 插入数据
        if len(sql_del+sql_insert) > 0:
            sql = ";\n".join(sql_del+sql_insert)
            mark = self.db_server.updateDataBySQL(sql)
            return mark, sql

if __name__=="__main__":
    db = "mysql,root/6tfc^YHN@ali2.jycch.com:3306/sodap"
    obj = DepartmentTags(db)


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

    def get_refrence_tags(self, file, open_format, code_format):
        # 获取TXT文件数据到列表中
        tags_data = self.list_filedata(file, open_format)
        print("原始文件数据列表：", tags_data)
        # 将列表数据按需要的格式进行解码
        tags_data = self.decode_data(tags_data, code_format)
        # 建立科室-标签字典
        dept_tags = {}
        for dept_tag in tags_data:
            dept_tag = dept_tag.replace("\n", "")  # 去除多余换行符
            dept_tag = dept_tag.replace("\r", "")
            dept_tag = dept_tag.replace(" ", "")
            dept_tags[dept_tag.split(":")[0]] = dept_tag.split(":")[1].split(",")
        return dept_tags

    def get_deptinfo(self):
        '''
        科室信息：科室id，科室名称，医院id，医院名称
        :return: 科室信息列表
        '''
        sql = "SELECT d.id,d.name,d.hospital_id,h.name FROM departments d,hospitals h WHERE d.is_deleted = 0 and d.hospital_id=h.id"
        list_depts = self.db_server.listDataBySQL(sql)
        return list_depts

    def get_taginfo(self):
        '''
        科室标签信息：科室id，科室名称，标签名称，标签id
        :return: 科室标签列表
        '''
        sql = "SELECT department_id,tag_name,tag_id FROM departmert_tag WHERE tag_name not in ('A+','A','B') and is_grade=0 ORDER BY department_id"
        list_tags = self.db_server.listDataBySQL(sql)
        return list_tags

    def assertTagsOfDepartments(self, list_depts, list_tags, ref_tags_dict):
        print list_depts
        msg = []
        for dept in list_depts:
            dept_id = dept[0]
            dept_name = dept[1]
            list_dept_tags = [list_tags[i][1] for i in range(len(list_tags)) if list_tags[i][0] == dept_id]
            list_dept_tags_ref = ref_tags_dict.get(dept_name,[])

            if len(list_dept_tags) == 0:  #数据库中未给该科室打标签
                # print ("%s(id:%d)-%s(id:%d) has no tag in db" % (dept[3],dept[2],dept_name,dept_id))
                msg.append("%s(id:%d)-%s(id:%d) has no tag in db" % (dept[3],dept[2],dept_name,dept_id))
                continue
            else:  #数据库中已经给该科室打标签
                if len(list_dept_tags_ref) == 0: #参照文件中不存在该科室的标签信息
                    # print ("%s(id:%d)-%s(id:%d) has no refrence tags in file" % (dept[3],dept[2],dept_name,dept_id))
                    msg.append("%s(id:%d)-%s(id:%d) has no refrence tags in file" % (dept[3],dept[2],dept_name,dept_id))
                    continue
                else:
                    missed_tags = [tag for tag in list_dept_tags_ref if tag not in list_dept_tags]
                    wrong_tags = [tag for tag in list_dept_tags if tag not in list_dept_tags_ref]
                    if len(missed_tags) > 0:
                        # print "1---"
                        # print ("%s(id:%d)-%s(id:%d)  in db missed tags:%s" % (dept[3],dept[2],dept_name,dept_id,",".join(missed_tags)))
                        msg.append("%s(id:%d)-%s(id:%d)  in db missed tags:%s" % (dept[3],dept[2],dept_name,dept_id,",".join(missed_tags)))

                    if len(wrong_tags) > 0:
                        # print "2---"
                        # print ("%s(id:%d)-%s(id:%d)  in db has wrong tags:%s" % (dept[3],dept[2],dept_name,dept_id,",".join(wrong_tags)))
                        msg.append("%s(id:%d)-%s(id:%d)  in db has wrong tags:%s" % (dept[3],dept[2],dept_name,dept_id,",".join(wrong_tags)))
        return msg



if __name__ == "__main__":
    db = "mysql,root/6tfc^YHN@10.0.127.16:3306/sodap"
    # file = "/Users/yan/PycharmProjects/TestTool/department_tags.txt"
    file = "C:\Users\Administrator\Desktop\department_tags.txt"
    open_format = "rb"
    code_format = "gb2312"
    deptServer = DepartmentTags(db)

    list_depts = deptServer.get_deptinfo()
    list_tags = deptServer.get_taginfo()
    ref_tags_dict = deptServer.get_refrence_tags(file, open_format, code_format)
    msg = deptServer.assertTagsOfDepartments(list_depts, list_tags, ref_tags_dict)
    if len(msg) > 0:
        mail_server = MailServer()
        receiver = ["1106045430@qq.com", "18108347985@163.com"]
        title = "科室标签差异信息"
        content = "\n".join(msg)
        mail_server.send_mail(receiver, title, content)

#encoding:utf-8
from DepartmentTags import DepartmentTags
from Common.MailServer.MailServer import MailServer
from Common.FileServer.FileServer import FileServer
class CompareTags(object):
    def __init__(self):
        pass
    def compareTags(self,db,file,mail_receiver=["18108347985@163.com"]):
        deptServer = DepartmentTags(db)
        open_format = "rb"
        depts_info = deptServer.get_deptinfo()
        depttags_info = deptServer.get_dept_taginfo()
        ref_tags_info = deptServer.get_refrence_tags(file, open_format)
        msg, untaged_depts, unchecked_depts, wrongtag_depts = deptServer.assertTagsOfDepartments(depts_info,
                                                                                                 depttags_info,
                                                                                                 ref_tags_info)
        if len(msg) > 1:
            print("*WARN*科室标签可能有误，请确认")
            for line in msg:
                print(line)
            mail_server = MailServer()
            receiver = mail_receiver
            title = "科室标签可能有误，请确认"
            content = "您好\n数据库中标签的科室可能有误，详情见附件\n数据库：%s" % db
            fileServer = FileServer()
            fileServer.write_list_to_excel(msg,"tag_check_result.xls",u"科室标签对比结果")
            attachment="tag_check_result.xls"
            # mail_server.send_mail(receiver, title, content,attachment)
            return untaged_depts+wrongtag_depts
        else:
            print "*INFO* department tags all right"
            return []

    def attachTags(self,db,file,depts=None,mail_receiver=["18108347985@163.com"]):
        if depts==None:
            depts=self.compareTags(db,file,mail_receiver)
        if len(depts) > 0:
            deptServer = DepartmentTags(db)
            tags_info = deptServer.get_taginfo()
            ref_tags_info = deptServer.get_refrence_tags(file,"rb")
            mark,sql = deptServer.attachTagsToDept(depts,tags_info,ref_tags_info)
            if mark:
                mail_server = MailServer()
                receiver = mail_receiver
                title = "更新数据库标签信息执行SQL"
                mail_server.send_mail(receiver,title,sql)
                print("*INFO*数据库更新成功")
                print sql

if __name__=="__main__":
    # file = "/Users/yan/PycharmProjects/TestTool/department_tags.txt"
    file = "C:\Users\Administrator\Desktop\department_tags.txt"
    # db = "mysql,root/123456@127.0.0.1:3306/null"
    db = "mysql,root/6tfc^YHN@ali2.jycch.com:3306/sodap"
    obj = CompareTags()
    # dept_check =obj.compareTags(db,file)
    obj.attachTags(db,file)
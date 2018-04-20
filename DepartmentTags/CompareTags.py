#encoding:
from DepartmentTags import DepartmentTags
class CompareTags(object):
    def __init__(self,db,file):
        self.db = db
        self.file = file
        self.deptServer = DepartmentTags(self.db)
    def compareTags(self):
        open_format = "rb"
        code_format = "gb2312"
        depts_info = self.deptServer.get_deptinfo()
        depttags_info = self.deptServer.get_dept_taginfo()
        ref_tags_info = self.deptServer.get_refrence_tags(self.file, open_format, code_format)
        msg, untaged_depts, unchecked_depts, wrongtag_depts = self.deptServer.assertTagsOfDepartments(depts_info,
                                                                                                 depttags_info,
                                                                                                 ref_tags_info)
        print "\n".join(msg)
        return msg, untaged_depts, unchecked_depts, wrongtag_depts

    def attachTags(self):
        open_format = "rb"
        code_format = "gb2312"
        depts_info = self.deptServer.get_deptinfo()
        depttags_info = self.deptServer.get_dept_taginfo()
        ref_tags_info = self.deptServer.get_refrence_tags(self.file, open_format, code_format)
        msg, untaged_depts, unchecked_depts, wrongtag_depts = self.deptServer.assertTagsOfDepartments(depts_info,
                                                                                                      depttags_info,
                                                                                                      ref_tags_info)
        if len(untaged_depts+wrongtag_depts) > 0:
            tags_info = self.deptServer.get_taginfo()
            self.deptServer.attachTagsToDept(untaged_depts+wrongtag_depts,tags_info,ref_tags_info)


if __name__=="__main__":
    # db = "mysql,root/6tfc^YHN@10.0.127.16:3306/sodap"
    # file = "/Users/yan/PycharmProjects/TestTool/department_tags.txt"
    file = "C:\Users\Administrator\Desktop\department_tags.txt"
    db = "mysql,root/6tfc^YHN@ali2.jycch.com:3306/sodap"
    # db = "mysql,root/6tfc^YHN@10.0.127.10:3306/sodap"
    obj = CompareTags(db,file)
    obj.compareTags()
    obj.
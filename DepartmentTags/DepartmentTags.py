#encoding:utf-8
from Common.FileServer.FileServer import FileServer
class DepartmentTags(object):
    def __init__(self):
        self.file_server = FileServer()

    def list_file_data(self,file,format):
        list_data = self.file_server.list_lines_data(file,format)
        return list_data

    def decode_listdata(self,list,format):
        return [element.decode(format) for element in list]

    def get_refrence_tags(self,file,open_format,code_format):
        #获取TXT文件数据到列表中
        tags_data = self.list_file_data(file,open_format)
        #将列表数据按需要的格式进行解码
        tags_data = self.decode_listdata(tags_data,code_format)
        #建立科室-标签字典
        dept_tags = {}
        for dept_tag in tags_data:
            dept_tag = str(dept_tag)
            dept_tag = dept_tag.replace("\n","")
            dept_tag = dept_tag.replace("\r","")
            dept_tag = dept_tag.replace(" ","")
            dept_tags[dept_tag.split(":")[0]] = dept_tag.split(":")[1]
        return dept_tags

if __name__=="__main__":
    deptServer = DepartmentTags()
    dept_tags = deptServer.get_refrence_tags("C:\zhuoyan_work\zhuoyan\PyCharm\DBCompare\test.txt","rb","utf-8")
    print dept_tags

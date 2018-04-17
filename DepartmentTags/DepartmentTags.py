#encoding:utf-8
import chardet
import uniout
from Common.FileServer.FileServer import FileServer
class DepartmentTags(object):
    def __init__(self):
        self.file_server = FileServer()

    def get_filedata(self,file,format):
        str_data = self.file_server.file_read(file,format)
        return str_data

    def list_filedata(self,file,format):
        list_data = self.file_server.file_readlines(file,format)
        return list_data

    def decode_data(self,data,code_format):
        if isinstance(data,str):
            return data.decode(code_format)
        elif isinstance(data,list):
            return [element.decode(code_format) for element in data]
        else:
            print("*ERROR* decode data type can only be str,list!")

    def get_refrence_tags(self,file,open_format,code_format):
        #获取TXT文件数据到列表中
        tags_data = self.list_filedata(file,open_format)
        print("原始文件数据列表：",tags_data)
        #将列表数据按需要的格式进行解码
        tags_data = self.decode_data(tags_data,code_format)
        #建立科室-标签字典
        dept_tags = {}
        for dept_tag in tags_data:
            dept_tag = dept_tag.replace("\n","") #去除多余换行符
            dept_tag = dept_tag.replace("\r","")
            dept_tag = dept_tag.replace(" ","")
            dept_tags[dept_tag.split(":")[0]] = dept_tag.split(":")[1]
        return dept_tags

if __name__=="__main__":
    file = "/Users/yan/PycharmProjects/TestTool/department_tags.txt"
    open_format = "rb"
    code_format = "gb2312"
    deptServer = DepartmentTags()
    dept_tags = deptServer.get_refrence_tags(file,open_format,code_format)
    print dept_tags

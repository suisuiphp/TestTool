# encoding:utf-8
import chardet,uniout
class FileServer(object):
    def __init__(self):
        pass

    @staticmethod
    def __file_open(filename, format):
        try:
            file = open(filename, format)
        except Exception as e:
            print("*ERROR* ", repr(e))
        return file

    @staticmethod
    def __file_close(file):
        if file != None:
            try:
                file.close()
            except Exception as e:
                print("*ERROR* ", repr(e))

    def file_readlines(self, filename, format):
        '''
        按行读取TXT文件中所以数据
        :param file:
        :param format:
        :return: 返回行数数据列表
        '''
        # 打开文件
        file = self.__file_open(filename, format)
        # 读文件到列表
        list_data = []
        if file != None:
            list_data = file.readlines()
        # 关闭文件
        self.__file_close(file)
        return list_data

    def file_read(self,filename,format):
        '''
        读取TXT文件中所有数据
        :param file:
        :param format:
        :return: str
        '''
        # 打开文件
        file = self.__file_open(filename, format)
        # 读文件到列表
        str_data = []
        if file != None:
            str_data = file.read()
        # 关闭文件
        self.__file_close(file)
        return str_data

    def fileWrite(self, filename, format, str):
        file = self.__file_open(filename, format)
        if file != None:
            try:
                file.write(str)
            except Exception as e:
                print("*ERROR*", repr(e))
            finally:
                self.__file_close(file)

    def get_encode_format(self,filename):
        file_data = self.file_read(filename,"rb")
        encode_info = chardet.detect(file_data)
        encode_format = encode_info.get("encoding")
        return encode_format


if __name__ == "__main__":
    file = "/Users/yan/PycharmProjects/TestTool/department_tags.txt"
    # file = "C:\Users\Administrator\Desktop\department_tags.txt"
    open_format = "rb"
    fileserver = FileServer()
    #
    # str_data = fileserver.file_read(file,open_format)
    # # print str_data.decode("gb2312")
    # list_data = str_data.split("\n")
    # print(list_data)
    #验证文件编码格式
    # f = open(file, "rb")
    # data = f.read()
    # print(chardet.detect(data))
    # f.close()
    encode_format=fileserver.get_encode_format(file)
    print(encode_format,type(encode_format))





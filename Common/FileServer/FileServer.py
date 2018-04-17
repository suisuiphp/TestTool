# encoding:utf-8
import chardet
class FileServer(object):
    def __init__(self):
        pass

    @staticmethod
    def __file_open(file, format):
        try:
            file = open(file, format)
        except Exception as e:
            print("*ERROR* ", repr(e))
        return file

    @staticmethod
    def __file_close(filename):
        if filename != None:
            try:
                file.close()
            except Exception as e:
                print("*ERROR* ", repr(e))

    def list_lines_data(self, file, format):
        '''
        按行读取TXT文件中所以数据
        :param file:
        :param format:
        :return: 返回行数数据列表
        '''
        # 打开文件
        print("start---")
        file = self.__file_open(file, format)
        # 读文件到列表
        list_data = []
        if file != None:
            list_data = file.readlines()
        # 关闭文件
        self.__file_close(file)
        return list_data

    def fileWrite(self, file, format, str):
        file = self.__file_open(file, format)
        if file != None:
            try:
                file.write(str)
            except Exception as e:
                print("*ERROR*", repr(e))
            finally:
                self.__file_close(file)


if __name__ == "__main__":

    fileserver = FileServer()
    list_data = fileserver.list_lines_data("C:\zhuoyan_work\zhuoyan\PyCharm\DBCompare\test.txt","rb")
    print list_data
    # file = fileserver.open("test.txt", "rb")
    # data = file.read()
    # print(chardet.detect(data))
    # print(data.decode("utf-8"))
    # try:
    #     file = open("tes.txt","rb")
    # except Exception as e:
    #     print("*ERROR* %s" % repr(e))
    # # file = open("tes.txt", "rb")
    # data_list = file.readlines()
    # file.close()
    # tag_deps = {}
    # for line in data_list:
    #     line = str(line.decode("utf-8"))
    #     line = line.replace("\n", "")
    #     line = line.replace("\r", "")
    #     line = line.replace(" ", "")
    #     tag_deps[line.split(":")[0]] = line.split(":")[1]
    # print(tag_deps)
    #
    # dep_tags = {"妇产科": "妇科", "感染科": "感染内科"}
    # for department, str_tags in dep_tags.items():
    #     print(department, str_tags)
    #     list_tags = str_tags.split(",")
    #     list_tags_ref = tag_deps.get(department).split(",")
    #     print("111", list_tags_ref)
    #     if list_tags_ref == None:
    #         print("unknown department")
    #     else:
    #         missed_tags = [tag for tag in list_tags_ref if tag not in list_tags]
    #         print("department:%s mistags:%s" % (department, ",".join(missed_tags)))

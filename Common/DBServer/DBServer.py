#encoding:utf-8
import pymysql
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class DBServer(object):
    #"oracle,pdwdata_uat/123456@10.20.112.123:1521/pdw"
    def __init__(self,db):
        self.dbtype = db.split(",")[0]
        self.db = db.split(",")[1]
        if self.dbtype.lower() not in ("mysql"):
            print("*ERROR* Database %s type can only be mysql" % self.db)
    def __connect(self):
        '''
        连接数据库,连接成功返回连接，否则退出程序
        '''
        if self.dbtype=="oracle":
            # connect = cx_Oracle.connect(self.db)
            pass
        if self.dbtype=="mysql":
            dbuser=self.db.split("/")[0]
            dbpasswd=self.db.split("/")[1].split("@")[0]
            dbhost=self.db.split("@")[1].split(":")[0]
            dbport=int(self.db.split(":")[1].split("/")[0])
            dbdatabase=self.db.split("/")[2]

            try:
                conn = pymysql.connect(user=dbuser,password=dbpasswd,host=dbhost,port=dbport,db=dbdatabase,charset="utf8")
                cur = conn.cursor()
                cur.execute("SET NAMES UTF8")
            except Exception as e:
                print("*ERROR*" + repr(e))
        return conn, cur

    def __close(self, connection, cursor):
        '''
        断开数据库连接
        :param connection: 数据库连接，cursor：游标
        :return:
        '''
        try:
            if cursor != None:
                cursor.close()
            if connection != None:
                connection.close()
        except Exception as e:
            print("*ERROR*" + repr(e))

    def listDataBySQL(self,str_sql):
        '''
        获取所有查询结果
        :param str_sql: var Str_sql
        :return: 返回List列表，列表中的元素为TUPLE类型
        '''
        conn,cur=self.__connect()
        list_rs=[]
        try:
            cur.execute(str_sql)
            list_rs=cur.fetchall()
        except Exception as e:
            print("*ERROR* ",repr(e))
        finally:
            self.__close(conn,cur)
        return list_rs

    def updateDataBySQL(self,str_sql):
        conn,cur = self.__connect()
        mark = False
        try:
            cur.execute(str_sql)
            conn.commit()
            mark = True
        except Exception as e:
            print ("*ERROR*" , repr(e))
        finally:
            self.__close(conn,cur)
        return mark

if __name__=="__main__":
    obj = DBServer("mysql,root/6tfc^YHN@ali2.jycch.com:3306/sodap")
    print obj
#encoding:utf-8
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class MailServer(object):

    def __init__(self,host="smtp.163.com",user="18108347985@163.com",passwd="20090704fei"):
        '''
        初始化邮件服务器，用户名和密码，当未传时，默认用163邮件服务器，发件邮箱为18108347985@163.com
        :param host: smtp.163.com 邮件服务器
        :param user: 邮箱登录用户名
        :param passwd: 邮箱登录密码
        '''
        self.mail_host = host
        self.mail_user = user
        self.mail_pass = passwd

    def send_mail(self,receivers,title,content,attachment=None):
        '''
        发送邮件
        :param receivers: ["1106045430@qq.com","18108347985@163.com"]收件人
        :param title: 邮件标题 str
        :param content: 邮件正文 str
        :param attachment: 附件路径"C:/GIT/TestTool/DepartmentTags/result.xls"
        :return:
        '''
        msg =  MIMEMultipart()
        msg["Subject"] = title
        msg["From"] = self.mail_user
        msg["To"] = ";".join(receivers)

        part = MIMEText(content,"plain", "utf-8")
        msg.attach(part)

        if attachment != None:
            part = MIMEApplication(open(attachment,"rb").read())
            part.add_header('Content-Disposition', 'attachment', filename=attachment)
            msg.attach(part)
        try:
            s = smtplib.SMTP()  #创建邮件服务器对象
            s.connect(self.mail_host, 25) #连接到指定的smtp服务器，参数分别表示smpt主机和端口
            s.login(self.mail_user, self.mail_pass)
            s.sendmail(self.mail_user, receivers, msg.as_string())
            print "*INFO* 邮件发送成功"
        except Exception as e:
            print "*ERROR* 无法发送邮件"
            print repr(e)
        finally:
            s.close()

# if __name__ == "__main__":
#     mail_server = MailServer()
#     receiver = ["1106045430@qq.com","18108347985@163.com"]
#     title = "放假通知"
#     content = "python mail test"
#     attachment = "C:/GIT/TestTool/DepartmentTags/result.xls"
#     mail_server.send_mail(receiver,title,content,attachment)



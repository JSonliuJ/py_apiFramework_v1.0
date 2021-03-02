# —— coding :utf-8 ——
# @time:    2020/9/23 21:14
# @IDE:     py_ApiTestFramework_V1.0
# @Author:  jsonJie
# @Email:   810030907@qq.com
# @File:    sendemail.py
# email：***@163.com password：***
"""
使用一个邮箱向另一个邮箱发送测试报告的html文件，这里需要对发送邮件的邮箱进行设置，获取邮箱授权码。
username=“发送邮件的邮箱”， password=“邮箱授权码”
这里要特别注意password不是邮箱密码而是邮箱授权码。
mail_server = "发送邮箱的服务器地址"
这里常用的有 qq邮箱——"stmp.qq.com", 163邮箱——"stmp.163.com"
其他邮箱服务器地址可自行百度
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

# 自动发送邮件
class SendEmail():
    def send_email(self, new_report):
        # 读取测试报告中的内容作为邮件的内容
        with open(new_report, 'r', encoding='utf8') as f:
            mail_body = f.read()
        # 发件人地址
        send_addr = '810030709@qq.com'
        # 收件人地址
        reciver_addr = 'jsonjie@163.com'
        # 发送邮箱的服务器地址 qq邮箱是'smtp.qq.com', 163邮箱是'smtp.163.com'
        mail_server = 'smtp.qq.com'
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        # 邮件标题
        subject = '接口自动化测试报告' + now
        # 发件人的邮箱及邮箱授权码
        username = '810030709@qq.com'
        password = 'moasmyxgojcgbbch'  # 注意这里是邮箱的授权码而不是邮箱密码
        # 邮箱的内容和标题
        message = MIMEText(mail_body, 'html', 'utf8')   # MIMEText(邮箱主体内容,内容类型,字符集）
        message['Subject'] = Header(subject, charset='utf8')
        # 发送邮件，使用的使smtp协议
        smtp = smtplib.SMTP()
        smtp.connect(mail_server)
        smtp.login(username, password)
        smtp.sendmail(send_addr, reciver_addr.split(','), message.as_string())
        smtp.quit()

    # 获取最新的测试报告地址
    def acquire_report_address(self, reports_address):
        # 测试报告文件夹中的所有文件加入到列表
        test_reports_list = os.listdir(reports_address)
        # 按照升序排序生成新的列表
        new_test_reports_list = sorted(test_reports_list)
        # 获取最新的测试报告
        the_last_report = new_test_reports_list[-1]
        # 最新的测试报告地址
        the_last_report_address = os.path.join(reports_address, the_last_report)
        return the_last_report_address




if __name__ == '__main__':
    # 测试报告存放位置
    from config.settings import dev_settings
    test_reports_address = dev_settings.html_report_path
    # 查找最新生成的测试报告地址
    new_report_addr = SendEmail().acquire_report_address(test_reports_address)
    # 自动发送邮件
    SendEmail().send_email(new_report_addr)
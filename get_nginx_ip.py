#!/usr/bin/python

import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header

file='/tmp/access.log'
mydict = {}
with open(file) as f:
        for line in f:
                match = re.match(r'([0-9]{1,3}\.){3}[0-9]{1,3}', line)
                if match:
                        ip = match.group()
                        if ip in mydict.keys():
                                mydict[ip] += 1
                        else:
                                mydict[ip] = 1

ipdict=sorted(mydict.items(),key=lambda item:item[1], reverse=True )[:10]
_ipfile=open('/tmp/ip.txt','w')
for x,y in ipdict:
    print("ip地址: %s,访问次数: %d"%(x,y),file=_ipfile)
_ipfile.close()

# 发件人和收件人
sender = 'xxxx@163.com'
receiver = 'xxxxxx@qq.com'

# 所使用的用来发送邮件的SMTP服务器
smtpServer = 'smtp.163.com'

# 发送邮箱的用户名和授权码
username = 'xxx@163.com'
password = 'xxxxxx'

mail_title = 'nginx访问IP统计TOP10'

#邮件正文
mail_body=open('/tmp/ip.txt').read()

message = MIMEText(mail_body, 'plain', 'utf-8') 
message['From'] = sender
message['To'] = receiver
message['Subject'] = Header(mail_title, 'utf-8') 

try:
    smtp = smtplib.SMTP() 
    smtp.connect(smtpServer)                      
    smtp.login(username, password)                
    smtp.sendmail(sender, receiver, message.as_string()) 
    print("邮件发送成功！！！")
    smtp.quit()
except smtplib.SMTPException:
    print("邮件发送失败！！！")
   
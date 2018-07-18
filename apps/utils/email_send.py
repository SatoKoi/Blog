# -*- coding:utf-8 -*-
import random
from email.mime.application import MIMEApplication

from users.models import EmailVarifyRecord
from itertools import chain
import smtplib
import email.mime.multipart
import email.mime.text
from django.core.mail import send_mail
from MyBlog.settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_FROM
from .common import super_range


def send_register_email(email, send_type="register", length=16, **kwargs):
    """发送邮件"""
    email_record, status = EmailVarifyRecord.objects.get_or_create(email=email, send_type=send_type)
    code = generate_random_code(length)
    token = generate_random_code(20)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.token = token
    email_record.save()                  # 保存邮箱验证码记录

    email_title = ""
    email_body = ""
    email_body_after = None
    username = kwargs.get("username")
    password = kwargs.get('password')
    if username and password:
        email_body_after = "\n用户名: {}\n密码: {}".format(username, password)
    if send_type == "register":
        email_title = "KoiSato邀请您注册激活链接"
        email_body = "请点击下方链接激活你的账号\n http://127.0.0.1:8000/active/{0}".format(code)
        if email_body_after:
            email_body += email_body_after
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # send_status = send_email(EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, email, email_title, email_body)       # 发送信息到目标邮箱里
        if send_status:     # 如果发送邮件成功
            pass
    elif send_type == "forget":
        email_title = 'KoiSato: 注册密码重置链接'
        email_body = "请点击下方链接激活重置你的密码\n http://127.0.0.1:8000/reset/{0}".format(code)
        if email_body_after:
            email_body += email_body_after
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # send_status = send_email(EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, email, email_title, email_body)
        if send_status:
            pass
    return token


def generate_random_code(random_length=8):
    """随机验证码生成"""
    chars = list(chain([str(i) for i in super_range(10)], super_range("A", "z")))
    random_code = ''
    for _ in super_range(random_length):
        random_code += random.choice(chars)
    return random_code


def send_email(smtpHost, sendAddr, password, recipientAddrs, subject='', content='', attachPart=None, attachPartName="附件"):
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = sendAddr
    msg['to'] = recipientAddrs
    msg['subject'] = subject
    txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)

    # 添加附件，传送D:/软件/yasuo.rar文件
    if attachPart:
        with open(attachPart, 'rb') as f:
            part = MIMEApplication(f.read())
            part.add_header('Content-Disposition', 'attachment', filename=attachPartName)
            msg.attach(part)

    smtp = smtplib.SMTP()
    smtp.connect(smtpHost, '25')
    smtp.login(sendAddr, password)
    smtp.sendmail(sendAddr, recipientAddrs, str(msg))
    smtp.quit()
    return True

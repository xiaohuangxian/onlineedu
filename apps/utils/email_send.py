# -*- coding: utf-8 -*-

from random import  Random


from users.models import EmailVerifyRecord
from django.core.mail import send_mail,EmailMessage
from onlineedu.settings import EMAIL_FROM
# 发送html格式的邮件:
from django.template import loader


def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(12)
    email_record.code =code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    #定义邮件内容
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "注册激活链接"
        email_body = "请打开以下地址激活账号：http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title ="找回密码链接"
        email_body = "请打开以下地址重置密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
        '''
        email_body = loader.render_to_string(
            "email_forget.html",{
                "active_code":code
            }
        )
        msg =EmailMessage(email_title,email_body,EMAIL_FROM,[email])
        msg.content_subtype ='html'
        send_status = msg.send()
        '''
    elif send_type == "update_email":
        email_title ="修改邮箱验证码"
        email_body = "您的邮箱验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
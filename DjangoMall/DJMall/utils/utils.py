import random
import string
from django.core.mail import BadHeaderError, send_mail
from django.http import JsonResponse, HttpResponseRedirect

'''
@file            :utils.py
@Description     :项目依赖的一些实用的小方法
@Date            :2021/12/23 10:22:19
@Author          :幸福关中 && 轻编程
@version         :v1.0
@GiteeUrl        :https://gitee.com/xingfugz/django-mall
'''

def random_str(randomlength=4):
    """ 生成4位数的随机字符串方法 """
    chars = string.ascii_letters + string.digits   # 生成a-zA-Z0-9字符串
    strcode = ''.join(random.sample(chars, randomlength))  # 生成随机的8位数字符串
    return strcode


def send_email(subject, message, to_emial=[], from_email="1158920674@qq.com"):
    # 发送邮件
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, to_emial)
        except BadHeaderError:
            return JsonResponse({'code': '失败！'})
        return JsonResponse({'code': '成功'})
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return JsonResponse({'message': '邮件格式有误！'})
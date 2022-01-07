from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class DJMallUser(AbstractUser):
    """ 用户模型 """
    nickename = models.CharField("昵称", max_length=50, blank=True, default="")
    signa = models.CharField("个性签名", max_length=50, blank=True, default="")
    phone = models.CharField("手机号", max_length=50, blank=True, default="")
    address = models.CharField("默认收货地址", max_length=50, blank=True, default="")
    desc = models.CharField("个人简介", max_length=200, blank=True, default="")

    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
    
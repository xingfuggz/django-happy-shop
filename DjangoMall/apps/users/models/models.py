from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class DJMallUser(AbstractUser):
    """ 用户模型 """
    phone = models.CharField("手机号", max_length=50)

    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    
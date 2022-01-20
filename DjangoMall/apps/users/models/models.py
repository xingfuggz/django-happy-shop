from django.db import models
from django.contrib.auth.models import AbstractUser
from DJMall.utils.models import DJMallBaseModel
from django.contrib.auth import get_user_model
# Create your models here.


class DJMallUser(AbstractUser):
    """ 用户模型 """
    nickename = models.CharField("昵称", max_length=50, blank=True, default="")
    signa = models.CharField("个性签名", max_length=50, blank=True, default="")
    phone = models.CharField("手机号", max_length=50, blank=True, default="")
    # address = models.CharField("默认收货地址", max_length=50, blank=True, default="")
    address = models.ForeignKey(
        'DJMallAddress', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        verbose_name="默认收货地址")
    desc = models.CharField("个人简介", max_length=200, blank=True, default="")
    avatar = models.ImageField("头像", upload_to='users/avatar/',
                               height_field=None, width_field=None, max_length=200, blank=True, null=True)

    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class DJMallAddress(DJMallBaseModel):
    """收货地址

    Args:
        DJMallBaseModel ([type]): [description]
    """
    owner = models.ForeignKey(DJMallUser, on_delete=models.DO_NOTHING, verbose_name="用户")
    name = models.CharField("签收人", max_length=50)
    phone = models.CharField("手机号", max_length=11)
    email = models.EmailField("邮箱", blank=True, default="", max_length=50)
    address = models.CharField(max_length=150, verbose_name="详细地址")
    is_default = models.BooleanField(default=False, verbose_name="设为默认")
    
    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} {self.address}'
    
    @classmethod
    def get_default(cls, user, is_default=True):
        """[获取默认收货地址]

        Args:
            user (request.user): 当前登录用户对象

        Returns:
            [Queryset]: 所属用户的默认收货地址的queryset数据
        """
        return cls.objects.filter(owner=user, is_default=is_default)
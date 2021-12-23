from django.db import models
from django.utils.translation import gettext_lazy as _
from DJMall.utils.models import DJMallBaseModel


class DJMallEmailVerifyRecord(DJMallBaseModel):

    class EmailChoices(models.TextChoices):
        REGISTER = 'ZC', _('Register')
        COMMENT = 'LY', _('Commment')

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=35)
    send_type = models.CharField(
        choices=EmailChoices.choices, default=EmailChoices.REGISTER, max_length=2)
    
    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

from django.db.models.signals import  post_save
from django.dispatch import receiver
from .models import DJMallUser


@receiver(post_save, sender=DJMallUser)
def create_djmalluser(sender, instance=None, created=False, **kwargs):
    # 添加用户及用户注册时自动将密码转为密文
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
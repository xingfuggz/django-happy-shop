from django.contrib.auth import get_user_model
# Register your models here.
from django.contrib.auth.models import Group


User = get_user_model()
from .admin import admin_site


# 注册模型站点
admin_site.register(User)
admin_site.register(Group)

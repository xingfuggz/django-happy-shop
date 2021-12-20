from django.contrib import admin
from django.contrib.admin import AdminSite
# Register your models here.
from .forms import DJMallAuthenticationForm


class DJMallAdminSite(AdminSite):
    # 自定义登录后台
    site_header = 'DJMall商城系统'
    site_title = '商城系统'
    login_form = DJMallAuthenticationForm
    login_template = 'dadmin/login.html'


admin_site = DJMallAdminSite(name='dadmin')




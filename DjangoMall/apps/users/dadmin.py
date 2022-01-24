'''
@file            :dadmin.py
@Description     :用户管理相关操作
@Date            :2022/01/25 00:27:14
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :mfhoudan
'''
from django.contrib import admin
from apps.dadmin.admin import admin_site

from .models import DJMallEmailVerifyRecord, DJMallFavorite, DJMallAddress

@admin.register(DJMallEmailVerifyRecord, site=admin_site)
class DJMallEmailVerifyRecordAdmin(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('id', 'code', 'add_date')
    

admin_site.register(DJMallFavorite)
admin_site.register(DJMallAddress)
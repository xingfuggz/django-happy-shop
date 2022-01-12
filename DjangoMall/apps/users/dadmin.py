
from django.contrib import admin
from apps.dadmin.admin import admin_site

from .models import DJMallEmailVerifyRecord, DJMallFavorite

@admin.register(DJMallEmailVerifyRecord, site=admin_site)
class DJMallEmailVerifyRecordAdmin(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('id', 'code', 'add_date')
    

admin_site.register(DJMallFavorite)
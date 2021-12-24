
from django.contrib import admin
from apps.dadmin.admin import admin_site

from .models import DJMallEmailVerifyRecord

@admin.register(DJMallEmailVerifyRecord, site=admin_site)
class DJMallEmailVerifyRecordAdmin(admin.ModelAdmin):
    '''Admin View for '''

    list_display = ('id', 'code', 'add_date')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)


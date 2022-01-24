from django.contrib import admin
from apps.dadmin.admin import admin_site
from django.utils.safestring import mark_safe
# Register your models here.
from .models import DJMallOrderInfo, DJMallOrderProduct


# admin_site.register(DJMallOrderInfo)
admin_site.register(DJMallOrderProduct)


@admin.register(DJMallOrderInfo, site=admin_site)
class DJMallOrderInfoAdmin(admin.ModelAdmin):
    '''Admin View for DJMallOrderInfo'''

    list_display = ('order_sn', 'get_product_sku', 'pay_status', 
                    'pay_method', 'total_amount', 'freight', 'pay_time', )
    list_filter = ('pay_status', 'pay_method')
    list_editable = ('pay_status',)
    readonly_fields = ('get_product_sku',)
   
    @admin.display(description='订单商品')
    def get_product_sku(self, obj):
        product_queryset = obj.djmallorderproduct_set.all()
        product_list = []
        for product in product_queryset:
            product_list.append('''
                <div style="float:left; width:50px; height: 50px; margin-right:5px">
                    <img src="{}" width="50" height="50" />
                </div> 
                '''.format(product.sku.main_picture.url))
            product_list.append(f'<div style="font-weight: 500;">{product.sku.spu.title}</div>')
            product_list.append(f'<div style="color:red">数量：{str(product.count)}</div>')
            options = [op[0] for op in list(product.sku.options.values_list('value'))]
            options = ','.join(options)
            product_list.append(f'<div style="color:red; margin-bottom: 15px;">规格：{options}</div>')
            product_list.append('<div style="clear:both"></div>')
            
        return mark_safe(''.join(product_list))
        
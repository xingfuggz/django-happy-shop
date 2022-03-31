from django.contrib import admin

# Register your models here.
from .models import (
    HappyShopCategory, HappyShopBrand, HappyShopSPU,
    HappyShopSKU, HappyShopSPUSpec, HappyShopSpecToOption,
    HappyShopSPUSpecOption, HappyShopSPUCarousel, HappyShopingCart, HappyShopOrderInfo,
    HappyShopOrderSKU, HappyShopBanner
)


class HappyShopAdmin(admin.ModelAdmin):
    '''Admin View for '''
    exclude = ('is_del',)
    

admin.site.register(HappyShopCategory)
admin.site.register(HappyShopBrand)
admin.site.register(HappyShopSPU)
# admin.site.register(HappyShopSKU)
admin.site.register(HappyShopSPUSpec)
admin.site.register(HappyShopSPUSpecOption)
admin.site.register(HappyShopSpecToOption)
admin.site.register(HappyShopSPUCarousel)
admin.site.register(HappyShopingCart)
# admin.site.register(HappyShopOrderInfo)
admin.site.register(HappyShopOrderSKU)
admin.site.register(HappyShopBanner)


@admin.register(HappyShopOrderInfo)
class HappyShopOrderInfoAdmin(HappyShopAdmin):
    '''Admin View for '''

    list_display = ('id', 'order_sn', 'trade_sn', 'pay_status', 'pay_method', 'total_amount', 'order_mark', 'freight', 'pay_time', 'is_del')
    list_editable = ('is_del', 'pay_status')

    # def get_queryset(self, request):
    #     return HappyShopOrderInfo.objects.filter(is_del=False)


@admin.register(HappyShopSKU)
class HappyShopSKUAdmin(HappyShopAdmin):
    '''Admin View for HappyShopSKU'''

    list_display = ('id', 'spu', 'main_picture', 'bar_code', 'sell_price', 'market_price', 'cost_price', 'stocks', 'sales', 'sort', )
    readonly_fields = ('sales',)
   
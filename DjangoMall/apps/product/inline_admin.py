from django.contrib import admin
from django.db.models import fields
from .models import DJMallProductCarouse, DJMallProductSKU, DJMallProductSPUSpecOption


class DJMallProductCarouseInlineAdmin(admin.TabularInline):
    model = DJMallProductCarouse
    extra = 3
    exclude = ('is_del',)


class DJMallProductSKUInlineAdmin(admin.StackedInline):
    model = DJMallProductSKU
    extra = 1
    fields = ('main_picture', 'bar_code', 'sell_price', 'market_price', 'cost_price', 'stocks', 'sales', 'options',)
    filter_horizontal = ('options', )


class DJMallProductSPUSpecOptionInlineAdmin(admin.TabularInline):
    model = DJMallProductSPUSpecOption
    extra = 1
    exclude = ('is_del',)
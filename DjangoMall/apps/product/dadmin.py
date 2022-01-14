from django.contrib import admin
# Register your models here.
from apps.dadmin.admin import admin_site
from product.models import (
    DJMallProductCategory, DJMallProductBrand, DJMallProductSPU,
    DJMallProductSPUSpec, DJMallProductSPUSpecOption, DJMallShopingCart)
from .inline_admin import (
    DJMallProductCarouseInlineAdmin, DJMallProductSKUInlineAdmin, 
    DJMallProductSPUSpecOptionInlineAdmin)


@admin.register(DJMallProductCategory, site=admin_site)
class DJMallProductCategoryAdmin(admin.ModelAdmin):
    '''Admin View for DJMallProductCategory'''

    list_display = ('id', 'name', 'parent', 'is_nav', 'sort', 'add_date')
    list_filter = ('name',)
    search_fields = ('name',)
    search_help_text = "请输入分类名称搜索",
    list_editable = ('sort', 'is_nav')
    # list_select_related的值应是布尔值、列表或元组。默认值是 False。减少关联关系查询数据库！
    list_select_related = ('parent',)
    save_as = False             # 保存并增加一个按钮变为另存为新的，相当于复制了一个，知识更改了自增id
    actions_on_top = True      # 列表页动作框位置控制
    actions_on_bottom = False

    # 编辑页面允许编辑的字段
    fields = ('parent', 'name', 'desc', 'icon', 'pc_img', 'sort', 'is_nav',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 过滤父级为顶级分类，这样在后台操作添加数据时就只能选择顶级分类
        if db_field.name == "parent":
            kwargs["queryset"] = DJMallProductCategory.objects.filter(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(DJMallProductBrand, site=admin_site)
class DJMallProductBrandAdmin(admin.ModelAdmin):
    '''Admin View for DJMallProductBrand'''

    list_display = ('id', 'name', 'add_date')
    list_filter = ('name',)
    search_fields = ('name',)
    exclude = ('is_del',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 品牌归属为顶级分类
        if db_field.name == "category":
            kwargs["queryset"] = DJMallProductCategory.objects.filter(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(DJMallProductSPU, site=admin_site)
class DJMallProductSPUAdmin(admin.ModelAdmin):
    '''Admin View for DJMallProductSPU'''

    list_display = ('id', 'title', 'sort', 'add_date')
    list_filter = ('title',)
    search_fields = ('title',)
    list_editable = ('sort',)
    readonly_fields = ('stocks', 'sales')
    inlines = [
        # DJMallProductSPUSpecInlineAdmin,
        DJMallProductSKUInlineAdmin,
        DJMallProductCarouseInlineAdmin,  
    ]
    fields = (
            'title', 'sub_title', 'desc', 'main_picture', 'brand', 
            ('is_new', 'is_hot', 'is_best', 'is_shelves'), 
            'category', 'content', 'after_services',
        )
    filter_horizontal = ('category', )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # 商品只能添加到二级分类
        if db_field.name == "category":
            kwargs["queryset"] = DJMallProductCategory.objects.exclude(parent=None)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(DJMallProductSPUSpec, site=admin_site)
class DJMallProductSPUSpecAdmin(admin.ModelAdmin):
    '''Admin View for DJMallProductSPUSpec'''

    list_display = ('id', 'name', 'add_date')
    list_filter = ('name',)
    search_fields = ('name',)
    inlines = [
        DJMallProductSPUSpecOptionInlineAdmin
    ]
    exclude = ('is_del',)


@admin.register(DJMallProductSPUSpecOption, site=admin_site)
class DJMallProductSPUSpecOptionAdmin(admin.ModelAdmin):
    '''Admin View for DJMallProductSPUSpecOption'''

    list_display = ('id', 'value', 'add_date')
    list_filter = ('value',)
    search_fields = ('value',)
    exclude = ('is_del',)
    
admin_site.register(DJMallShopingCart)
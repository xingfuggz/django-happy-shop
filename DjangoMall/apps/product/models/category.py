from django.db import models
from DJMall.utils import DJMallBaseModel

# Create your models here.


class DJMallProductCategory(DJMallBaseModel):
    """ 商品分类 """
    
    name = models.CharField("分类名称", max_length=50)
    desc = models.CharField("分类描述", max_length=100, blank=True, default="")
    parent = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        verbose_name="父级分类"
    )
    icon = models.ImageField(
        "分类图标", 
        upload_to="product/category/icon/", 
        blank=True,
        null=True,
        max_length=200)
    pc_img = models.ImageField(
        "首页楼层背景", 
        upload_to="product/category/pc/img/", 
        blank=True,
        null=True,
        height_field=None, 
        width_field=None, 
        max_length=200)
    is_nav = models.BooleanField("是否为导航", default=False)
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        db_table = 'd_product_category'
        ordering = ['-sort']
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.name



class DJMallProductBrand(DJMallBaseModel):
    """ 商品品牌 """

    category = models.ForeignKey(DJMallProductCategory, on_delete=models.CASCADE, verbose_name="所属分类")
    name = models.CharField("品牌名称", max_length=50)
    desc = models.CharField("品牌描述", max_length=100, blank=True, default="")
    logo = models.ImageField(
        "品牌logo", 
        upload_to="product/brand/logo/", 
        max_length=200, blank=True, null=True
    )
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        db_table = 'd_product_brand'
        ordering = ['-sort']
        verbose_name = "商品品牌"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.name
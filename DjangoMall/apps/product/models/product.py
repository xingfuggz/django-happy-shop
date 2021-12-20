from django.db import models
from DJMall.utils import DJMallBaseModel
from .category import DJMallProductBrand, DJMallProductCategory


class DJMallProductSPU(DJMallBaseModel):
    """ 商品SPU """
    title = models.CharField("商品标题", max_length=60)
    sub_title = models.CharField("商品副标题", max_length=100)
    desc = models.CharField("商品简介", max_length=150, blank=True, null=True)
    main_picture = models.ImageField("商品主图", upload_to="product/main/picture/spu/", max_length=200)
    stocks = models.PositiveIntegerField("总库存", default=0)
    sales = models.PositiveIntegerField("总销量", default=0)
    content = models.TextField("商品详情")
    category = models.ManyToManyField(DJMallProductCategory, verbose_name="商品分类")
    brand = models.ForeignKey(DJMallProductBrand, on_delete=models.CASCADE, verbose_name="商品品牌")
    is_new = models.BooleanField("是否新品", default=False)
    is_hot = models.BooleanField("是否热销", default=False)
    is_best = models.BooleanField("是否精品", default=False)
    is_shelves = models.BooleanField("是否促销", default=False)
    after_services = models.TextField("售后说明", default="", blank=True)
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        db_table = 'd_product_spu'
        ordering = ['-sort']
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.title


class DJMallProductSKU(DJMallBaseModel):
    """ 商品SKU """
    spu = models.ForeignKey(DJMallProductSPU, on_delete=models.CASCADE, verbose_name="商品")
    options = models.ManyToManyField('DJMallProductSPUSpecOption', blank=True, verbose_name="规格值")
    main_picture = models.ImageField(
        "商品主图", upload_to="product/main/picture/sku/", max_length=200)
    bar_code = models.CharField("商品条码", max_length=50, default="", blank=True)
    sell_price = models.DecimalField("商品售价", max_digits=8, decimal_places=2)
    market_price = models.DecimalField("市场价/划线价", max_digits=8, decimal_places=2)
    cost_price = models.DecimalField("成本价", max_digits=8, decimal_places=2)
    stocks = models.PositiveIntegerField("库存", default=0)
    sales = models.PositiveIntegerField("销量", default=0)
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        db_table = 'd_product_sku'
        ordering = ['-sort']
        verbose_name = "商品SKU"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return f'{self.spu.title} {self.options}'


class DJMallProductSPUSpec(DJMallBaseModel):
    """ 商品规格选项 """
    spu = models.ForeignKey(
        DJMallProductSPU, 
        on_delete=models.CASCADE, 
        verbose_name="商品"
    )
    name = models.CharField("规格名称", max_length=50)

    class Meta:
        db_table = 'd_product_spu_spec'
        ordering = ['-add_date']
        verbose_name = "商品规格"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return f'{self.spu.title}的规格 {self.name}'


class DJMallProductSPUSpecOption(DJMallBaseModel):
    """ 商品规格值 """
    spec = models.ForeignKey(
        DJMallProductSPUSpec, 
        on_delete=models.CASCADE, 
        verbose_name="规格"
    )
    value = models.CharField("规格值", max_length=50)

    class Meta:
        db_table = 'd_product_spu_spec_option'
        ordering = ['-add_date']
        verbose_name = "商品规格值"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return f'【{self.spec.name}】：{self.value}'


class DJMallProductCarouse(DJMallBaseModel):
    """ 商品轮播图 """
    spu = models.ForeignKey(
        DJMallProductSPU, 
        on_delete=models.CASCADE, 
        verbose_name="商品"
    )
    img = models.ImageField("轮播图", upload_to="product/carouse/img/", max_length=200)
    img_url = models.CharField("外链图片", max_length=50, default="", blank=True)
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        db_table = 'd_product_carouse'
        ordering = ['-sort']
        verbose_name = "商品轮播图"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return f'{self.spu.title}的轮播图{self.img}'

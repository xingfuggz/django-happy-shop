from django_filters import rest_framework as filters
from happy_shop.models import  HappyShopSKU, HappyShopSPU, HappyShopCategory


class HappyShopSPUFilter(filters.FilterSet):
    """SPU 筛选"""
    order = filters.OrderingFilter(fields=('skus__sell_price',))

    class Meta:
        model = HappyShopSPU
        fields = ['brand', 'is_new', 'is_hot', 'is_best', 'category', 'is_shelves']


class HappyShopSKUFilter(filters.FilterSet):
    """ 过滤sku """
    order = filters.OrderingFilter(fields=('sell_price',))

    class Meta:
        model = HappyShopSKU
        fields = ['spu__brand', 'spu__is_new', 'spu__is_hot', 'spu__is_best', 'spu__is_shelves', 'spu__category']


class HappyShopCategoryFilter(filters.FilterSet):

    class Meta:
        model = HappyShopCategory
        fields = ['is_nav', ]

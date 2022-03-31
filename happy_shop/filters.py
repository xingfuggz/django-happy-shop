import django_filters
from happy_shop.models import HappyShopCategory, HappyShopSPU, HappyShopSKU


class HappyShopSPUFilter(django_filters.FilterSet):
    
    order = django_filters.OrderingFilter(fields=('skus__sell_price',))

    class Meta:
        model = HappyShopSPU
        fields = ['brand', 'is_new', 'is_hot', 'is_best', 'is_shelves']


class HappyShopSKUFilter(django_filters.FilterSet):
    
    order = django_filters.OrderingFilter(fields=('sell_price',))

    class Meta:
        model = HappyShopSKU
        fields = ['spu__brand', 'spu__is_new', 'spu__is_hot', 'spu__is_best', 'spu__is_shelves']
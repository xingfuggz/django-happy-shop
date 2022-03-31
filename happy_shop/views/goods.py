from django.views.generic import TemplateView, DetailView
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
# from django.conf import settings
from happy_shop.conf import happy_shop_settings
from happy_shop.models import HappyShopCategory, HappyShopSPU, HappyShopBrand, HappyShopSKU
from happy_shop.filters import HappyShopSPUFilter, HappyShopSKUFilter

from .views import BaseView


class IndexView(BaseView, TemplateView):
    """首页视图"""
    template_name = 'happy_shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cate_skus_dict'] = self.get_cate_skus()
        return context
    
    def get_cate_skus(self):
        parent_cates = HappyShopCategory.objects.filter(parent__isnull=True, is_nav=True)
        cate_skus_dict = {}
        for cate in parent_cates:
            sub_cates = cate.sub_cates.filter(is_del=False, is_nav=True).values_list('id', flat=True)
            skus = HappyShopSKU.objects.filter(spu__category__id__in=list(sub_cates)).distinct()
            print(skus)
            cate_skus_dict[cate.name] = skus[:happy_shop_settings.FLOOR_NUM]
        return cate_skus_dict


class HappyShopCategoryView(BaseView, SingleObjectMixin, ListView):
    """ 商品列表页即商品分类详情页
    最终返回的是当前分类下的sku的queryset数据
    """
    template_name = "happy_shop/goods.html"
    paginate_by = happy_shop_settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        # 当前分类数据
        self.object = self.get_object(queryset=HappyShopCategory.objects.filter(is_del=False))
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        qs_filter = self.get_filter_queryset()
        queryset = qs_filter.qs
        return queryset
    
    def get_filter_queryset(self):
        """ 筛选过的数据 """
        spus = self.object.spu_cates.filter(is_del=False)
        skus_id = []
        for spu in spus:
            skus_id += list(spu.skus.values_list('id', flat=True))
        queryset = HappyShopSKU.objects.filter(id__in=skus_id, is_del=False)
        return HappyShopSKUFilter(self.request.GET, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goods'] = self.get_filter_queryset()
        context['brands'] = self.get_brands()
        context['category'] = self.object

        if self.request.GET.get('brand'):
            context['brand_id'] = int(self.request.GET.get('brand'))
        else:
            context['brand_id'] = None
        return context
    
    def get_brands(self):
        """ 当前分类的品牌数据 """
        return self.object.brand_cates.filter(is_del=False)


class HappyShopSPUDetailView(BaseView, DetailView):
    """ 商品详情页
    """
    queryset = HappyShopSPU.objects.filter(is_del=False)
    template_name = 'happy_shop/detail.html'
    context_object_name = 'spu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goods_news'] = self.get_goods()[:happy_shop_settings.NEW_NUM]
        return context

    def get_goods(self):
        # 新品推荐
        cates = self.get_object().category.filter(is_del=False)
        skus_id = []
        for cate in cates:
            spus = cate.spu_cates.filter(is_del=False, is_new=True)
            for spu in spus:
                skus_id += list(spu.skus.values_list('id', flat=True))
        queryset = HappyShopSKU.objects.filter(id__in=list(set(skus_id)), is_del=False)
        if not queryset:
            queryset = self.get_object().skus.filter(is_del=False)
        return queryset
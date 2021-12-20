from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from DJMall.utils.views import DJMallBaseView
# Create your views here.
from product.models import DJMallProductCategory
from product.models.product import DJMallProductSPU


class DJMallProductCategoryListView(DJMallBaseView, TemplateView):
    """ 商品全部分类页 """
    template_name = 'product/category.html'


class DJMallProductCategoryView(DJMallBaseView, SingleObjectMixin, ListView):
    """ 商品列表页即商品分类详情页 """
    template_name = "product/category_detail.html"
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        # 当前分类数据
        self.object = self.get_object(queryset=DJMallProductCategory.objects.all())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        context['pages'] = [i for i in context['paginator'].get_elided_page_range()]
        context['sort_dict'] = self.request.GET
        return context
    
    def get_queryset(self):
        """ 商品列表页数据结构
        @spu_queryset 
        - 当前分类下的商品Queryset数据,
        - 顶级分类返回所有二级分类商品的总和
        - 二级分类返回当前分类下的Queryset数据
        return queryset ==> [{spu:sku},{spu:sku}]
        """
        queryset = []
        spu_queryset = None
        if self.object.parent:
            # 二级分类下的筛选数据
            spu_queryset = self.object.djmallproductspu_set.all()
            spu_queryset = self.get_sort_queryset(self.object.djmallproductspu_set.all(), 'djmallproductsku__sell_price')
            spu_queryset = self.get_sort_queryset(self.object.djmallproductspu_set.all(), 'djmallproductsku__sales')
        else:
            # 顶级分类下返回所有的商品数据
            if self.request.GET and self.request.GET.get('djmallproductsku__sell_price'):
                spu_queryset = self.get_spu_queryset('djmallproductsku__sell_price')
            elif self.request.GET and self.request.GET.get('djmallproductsku__sales'):
                spu_queryset = self.get_spu_queryset('djmallproductsku__sales')
            else:
                spu_queryset = DJMallProductSPU.objects.filter(id__in=self.get_parent_spu_id())

        if spu_queryset:
            for product in spu_queryset:
                # 数据结构 {'spu': 'sku' }
                product_dict = {}
                product_dict[product] = product.djmallproductsku_set.first()
                queryset.append(product_dict)
        else:
            spu_queryset = []
        return queryset 
    
    def get_sort_queryset(self, queryset, field):
        # 根据指定的字段排序方法
        queryset = queryset
        field = self.request.GET.get(field)
        if field and field == field:
            queryset = queryset.order_by(field)  # 升序
        elif field == f'-{field}':
            queryset = queryset.order_by(f'-{field}')  # 降序
        else:
            queryset
        return queryset

    def get_parent_spu_id(self, q_list=[]):
        # 顶级分类下所有子类包含的商品id的list
        for sub_cate in self.object.djmallproductcategory_set.all():
            qs = sub_cate.djmallproductspu_set.all()
            for q in qs:
                q_list.append(q.id)
        return q_list

    def get_spu_queryset(self, field):
        # 顶级分类下所有子类包含的商品排序并返回
        # field 需要根据该字段，支持跨表查询写法filed__name
        parent_spu_queryset = DJMallProductSPU.objects.filter(id__in=self.get_parent_spu_id())
        spu_queryset = self.get_sort_queryset(parent_spu_queryset, field)
        return spu_queryset
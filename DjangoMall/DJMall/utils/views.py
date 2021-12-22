from django.views.generic import TemplateView
from product.models import DJMallProductCategory


class DJMallBaseView:
    """ 全局继承基类视图 """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_dict'] = dict(self.get_category_dict())
        return context
    
    def get_category_dict(self):
        # {'海鲜水产'：['鱼类', '虾类']}
        category_dict = {}
        category_queryset = DJMallProductCategory.objects.all()
        for category in category_queryset:    
            if category and category.parent is None:
                category_dict[category] = category.djmallproductcategory_set.all()
        
        return category_dict


class IndexTemplateView(DJMallBaseView, TemplateView):
    """ 首页视图 """
    template_name = "index.html"

from django.forms import forms
from django.http import JsonResponse
from django.views.generic import TemplateView
from product.models import DJMallProductCategory, DJMallShopingCart


class DJMallBaseView:
    """ 全局继承基类视图 """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_dict'] = dict(self.get_category_dict())
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
            context['cart_count'] = DJMallShopingCart.get_cart_count(self.request.user)
        return context
    
    def get_category_dict(self):
        # {'海鲜水产'：['鱼类', '虾类']}
        category_dict = {}
        category_queryset = DJMallProductCategory.objects.all()
        for category in category_queryset:    
            if category and category.parent is None:
                category_dict[category] = category.djmallproductcategory_set.all()
        return category_dict
        

class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {
                'pk': self.object.pk,
            }
            print('ceshi 49')
            return JsonResponse(data)


class IndexTemplateView(DJMallBaseView, TemplateView):
    """ 首页视图 """
    template_name = "index.html"

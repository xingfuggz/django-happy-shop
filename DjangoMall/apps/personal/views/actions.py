from django.views.generic import ListView, DeleteView, CreateView
from django.urls import reverse_lazy
from DJMall.utils.views import DJMallBaseView
from .views import DJMallLoginRequiredMixin
from users.models import DJMallFavorite, DJMallAddress


class DJMallFavoriteListView(DJMallLoginRequiredMixin, DJMallBaseView, ListView):
    # 收藏列表
    # model = DJMallFavorite
    template_name = "personal/fav_list.html"
    context_object_name = 'fav_list'
    paginate_by = 8

    def get_queryset(self):
        return DJMallFavorite.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = [i for i in context['paginator'].get_elided_page_range()]
        return context
    

class DJMallFavoriteDeleteView(DJMallLoginRequiredMixin, DJMallBaseView, DeleteView):
    # 删除收藏
    template_name = 'personal/delete.html'
    success_url = reverse_lazy('personal:fav_list')
    
    def get_queryset(self):
        return DJMallFavorite.objects.filter(owner=self.request.user)


class DJMallAddressListView(DJMallLoginRequiredMixin, DJMallBaseView, ListView):
    """地址列表

    Args:
        DJMallLoginRequiredMixin ([type]): [登录权限验证]
        DJMallBaseView ([type]): [全局继承基类]
        ListView ([type]): [列表类视图]

    Returns:
        [type]: [description]
    """
    template_name = "personal/list_address.html"
    context_object_name = "address_list"
        
    def get_queryset(self):
        return DJMallAddress.objects.filter(owner=self.request.user)


class DJMallAddressCreateView(DJMallLoginRequiredMixin, DJMallBaseView, CreateView):
    template_name = "personal/create_address.html"
    success_url = reverse_lazy('personal:address_list')
    
    def get_queryset(self):
        return DJMallAddress.objects.filter(owner=self.request.user)
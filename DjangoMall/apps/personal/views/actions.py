from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
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


class DJMallAddressUpdateView(DJMallLoginRequiredMixin, DJMallBaseView, UpdateView):
    # 修改地址
    template_name = "personal/update_address.html"
    success_url = reverse_lazy('personal:address_list')
    fields = ['name', 'phone', 'email', 'address', 'is_default']
    
    def get_queryset(self):
        return DJMallAddress.objects.filter(owner=self.request.user)
    
    def form_valid(self, form):
        user = self.request.user
        is_default = form.cleaned_data['is_default']
        address = DJMallAddress.get_default(user)
        if is_default and address.exists():
            address.update(is_default=False)
            user.address = self.get_object()
            user.save()
        elif is_default:
            user.address = self.get_object()
            user.save()
        elif not address.exists() and user.address:
            addr = DJMallAddress.objects.get(id=user.address.id)
            addr.is_default = True
            addr.save()
        else:
            addr = DJMallAddress.objects.first()
            addr.is_default = True
            addr.save()
            user.address = addr
            user.save()
        return super().form_valid(form)
    

class DJMallAddressCreateView(DJMallLoginRequiredMixin, DJMallBaseView, CreateView):
    # 新增地址
    template_name = "personal/create_address.html"
    success_url = reverse_lazy('personal:address_list')
    fields = ['name', 'phone', 'email', 'address', 'is_default']
    
    def get_queryset(self):
        return DJMallAddress.objects.filter(owner=self.request.user)
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = self.request.user
        is_default = form.cleaned_data['is_default']
        address = DJMallAddress.get_default(self.request.user)
        if is_default and address:
            address.update(is_default=False)
            addr = form.save(commit=False) 
            user.address = addr
            addr.save()
            user.save()
        elif is_default:
            addr = form.save(commit=False) 
            user.address = addr
            addr.save()
            user.save()
        return super().form_valid(form)    


class DJMallAddressDefaultUpdateView(DJMallAddressUpdateView):
    # 修改为默认
    template_name = "personal/update_address.html"
    success_url = reverse_lazy('personal:address_list')
    fields = ['is_default']
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.is_default = True
        address = DJMallAddress.get_default(self.request.user)
        if address:
            address.update(is_default=False)
            addr = form.save(commit=False) 
            user.address = addr
            addr.save()
            user.save()
        else:
            addr = form.save(commit=False) 
            user.address = addr
            addr.save()
            user.save()
        return JsonResponse({'code': 'ok', 'message': '设置成功'})
    

class DJMallAddressDeleteView(DJMallLoginRequiredMixin, DJMallBaseView, DeleteView):
    # 删除地址
    template_name = 'personal/delete.html'
    success_url = reverse_lazy('personal:address_list')
    
    def get_queryset(self):
        return DJMallAddress.objects.filter(owner=self.request.user)
    
    def form_valid(self, form):
        print('ceshi')
        return super().form_valid(form)
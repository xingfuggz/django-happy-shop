from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from DJMall.utils.views import DJMallBaseView
from .views import DJMallLoginRequiredMixin
from users.models import DJMallFavorite


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
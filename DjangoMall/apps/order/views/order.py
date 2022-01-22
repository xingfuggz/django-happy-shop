from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.cache import cache
from django.utils import timezone

from order.models import DJMallOrderInfo
from personal.views import DJMallLoginRequiredMixin
from DJMall.utils.views import DJMallBaseView
from users.models import DJMallAddress
from order.forms import DJMallOrderInfoForm, DJMallOrderProductForm


class DJMallOrderInfoView(DJMallLoginRequiredMixin, DJMallBaseView, CreateView):
    
    model = DJMallOrderInfo
    template_name = 'order/orderinfo.html'
    form_class = DJMallOrderInfoForm
    success_url = reverse_lazy('author-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pay_method'] = DJMallOrderInfo.get_pay_method()
        context['pay_default'] = DJMallOrderInfo.get_pay_default()
        context['address_list'] = DJMallAddress.objects.filter(owner=self.request.user)
        context['product_form'] = DJMallOrderProductForm()
        return context
    
    def form_valid(self, form):
        # form.initial
        print(form.initial)
        form.instance.owner = self.request.user
        form.instance.order_sn = self.get_order_sn()
        address = form.cleaned_data['address']
        print(address)
        # form.instance.address = form.cleaned_data['address']
        # return super().form_valid(form)
    
    def get_order_sn(self):
        # 生成订单号
        order_sn = timezone.now().strftime('%Y%m%d%H%M%S') + '%09d' % self.request.user.id
        return order_sn



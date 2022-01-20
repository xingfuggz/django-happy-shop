from django.shortcuts import render
from django.views.generic import TemplateView
from personal.views import DJMallLoginRequiredMixin
from DJMall.utils.views import DJMallBaseView
# Create your views here.
from users.models import DJMallAddress
from .models import DJMallOrderInfo


class DJMallPayView(DJMallLoginRequiredMixin, DJMallBaseView, TemplateView):
    """支付视图"""
    http_method_names = ['get', 'post']
    template_name = 'order/pay.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pay_method'] = DJMallOrderInfo.get_pay_method()
        context['pay_default'] = DJMallOrderInfo.get_pay_default()
        context['address_list'] = DJMallAddress.objects.filter(owner=self.request.user)
        return context
    
    
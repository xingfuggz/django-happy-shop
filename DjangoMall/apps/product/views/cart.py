import json
from decimal import Decimal
from re import S, template
from django.db import IntegrityError
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView
from django.core.cache import cache
from django.utils.safestring import mark_safe
from DJMall.utils.views import DJMallBaseView
from product.models import DJMallShopingCart, DJMallProductSKU
from personal.views import DJMallLoginRequiredMixin
from config.conf import DEL_STOCK_TIMING


class DJMallShopingCartView(DJMallLoginRequiredMixin, DJMallBaseView, TemplateView):
    # 加入购物车
    http_method_names = ['get', 'post']
    template_name = 'product/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = self.get_carts()
        return context
    
    def get_carts(self):
        carts = DJMallShopingCart.objects.filter(owner=self.request.user).values(
            'id', 'sku__id', 'sku__main_picture', 'sku__spu__title', 'sku__sell_price', 'num', "sku__stocks",)
        for index, cart in enumerate(carts):
            cart['index'] = index + 1
            cart['sku__sell_price'] = cart['sku__sell_price'].to_eng_string()
            cart['sku__main_picture'] = '/{}'.format(cart['sku__main_picture'])
            cart['sku_total_price'] = (Decimal(cart['sku__sell_price']) * cart['num']).to_eng_string()
            options = list(DJMallProductSKU.objects.get(id=cart['sku__id']).options.values_list('value'))
            cart['sku_options'] = ' , '.join([op[0] for op in options])
        # print(carts)
        carts = json.dumps(list(carts), ensure_ascii=False)
        # print(carts)
        return carts
        
    def post(self, request, *args, **kwargs):
        # 加入购物车
        sku_id = request.POST.get('sku_id')
        sku = DJMallProductSKU.objects.get(id=int(sku_id))
        num = request.POST.get('num')
        try:
            DJMallShopingCart.objects.create(owner=request.user, sku=sku, num=int(num))
            self.del_stock(sku, num)
            return JsonResponse({'code': 'ok', 'message': '已加入购物车！','stocks': sku.stocks})
        except IntegrityError:
            self.del_stock(sku, num)
            DJMallShopingCart.objects.filter(owner=request.user, sku=sku).update(num=F('num') + int(num))
            return JsonResponse({'code': 'ok', 'message': '该商品已在购物车，数量已增加！','stocks': sku.stocks})
        # return render(request, 'product/cart.html', {})
        
    def del_stock(self, sku, num, time=DEL_STOCK_TIMING):
        # 减库存操作
        # time为0时加购减库存
        if not time:
            sku.stocks -= int(num)
            sku.save()
            
class DJMallShopingCartDeleteView(DJMallLoginRequiredMixin, DeleteView):
     # 删除购物车
    template_name = 'personal/delete.html'
    success_url = reverse_lazy('product:cart')
    
    def get_queryset(self):
        return DJMallShopingCart.objects.filter(owner=self.request.user)
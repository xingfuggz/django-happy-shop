from django.db import IntegrityError
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.core.cache import cache
from product.models import DJMallShopingCart, DJMallProductSKU
from personal.views import DJMallLoginRequiredMixin
from config.conf import DEL_STOCK_TIMING


class DJMallShopingCartView(DJMallLoginRequiredMixin, View):
    # 加入购物车
    def get(self, request, *args, **kwargs):
        return render(request, 'product/cart.html', {})
        
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
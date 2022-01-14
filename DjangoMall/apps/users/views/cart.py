from django.shortcuts import render
from django.views.generic import View
from django.core.cache import cache


class DJMallShopingCartView(View):
    # 加入购物车
    def get(self, request, *args, **kwargs):
        cache.set('key', '这是一个值', 30)
        print(cache.get('key'))
        return render(request, 'users/cart.html', {})
        
    
    def post(self, request, *args, **kwargs):
        pass
import json
from decimal import Decimal
from django.db.models import F
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from django.utils import timezone
from django.views.generic import TemplateView
from personal.views import DJMallLoginRequiredMixin
from DJMall.utils.views import DJMallBaseView
from config.conf import DEL_STOCK_TIMING

# Create your views here.
from users.models import DJMallAddress
from product.models import DJMallProductSKU
from order.models import DJMallOrderInfo, DJMallOrderProduct


class DJMallPayView(DJMallLoginRequiredMixin, DJMallBaseView, TemplateView):
    """支付视图"""
    http_method_names = ['get', 'post']
    template_name = 'order/pay.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pay_method'] = DJMallOrderInfo.get_pay_method()
        context['pay_default'] = DJMallOrderInfo.get_pay_default()
        context['address_list'] = DJMallAddress.objects.filter(owner=self.request.user)
        context['carts'] = self.get_carts()
        context['type'] = self.get_type()
        return context
    
    def post(self, request, *args, **kwargs):
        # 获取到购物车数据放入缓存，永不过期，支付完成后主动清除缓存
        data = request.POST
        
        #  第一次POST请求购物车点击去支付按钮时传送的数据并缓存 #
        #####################################################
        # @is_type 拥有两个值
        # -- cache 为缓存标识，可以将其缓存
        # -- cart  为支付标识，代表支付的商品数据来自购物车
        is_type = data.get('type')
        carts = data.get('carts')
        # 缓存时机判断，这里如果不做判断，两次POST会覆盖缓存
        if is_type == 'cache' and carts:
            cache.set(request.user.id, carts, timeout=None) 
        ######################################################
        
        # 第二次type为cart表明为购物车数据支付    
        if is_type == 'cart' and self.get_carts():
            pay_method = data.get('pay_method')
            order_mark = data.get('order_mark')
            # address = DJMallAddress.objects.get(id=data.get('address')).address
            address = data.get('address')
            # 商品总金额，不含运费
            total_amount = self.get_sku_total_price(json.loads(self.get_carts()))
            # 订单号
            order_sn = self.get_order_sn()
            for cart in json.loads(self.get_carts()):
                sku = DJMallProductSKU.objects.get(id=int(cart.get('sku__id')))
                if sku.stocks > int(cart.get('num')):  # 减库存
                    self.del_stock(sku, int(cart.get('num')))
                    order = DJMallOrderInfo.objects.create(
                        owner=request.user,
                        order_sn=order_sn,
                        pay_method=pay_method,
                        total_amount=total_amount,
                        address=address,
                        order_mark=order_mark,
                        freight=0
                    )
                    DJMallOrderProduct.objects.create(
                        order = order,
                        sku = sku,
                        count = int(cart.get('num')),
                        price = Decimal(cart.get('sku__sell_price'))
                    )
                else:
                    return JsonResponse({'code': 'err', 'message': f'{sku}的库存不足！'})
                    # return render(request, 'order/pay.html', {'sku': sku})
                
        return JsonResponse({'message': 'ceshi'})
    
    def get_carts(self):
        """从缓存中读取购物车信息
        开发时使用内存缓存：每次服务器重载缓存信息会丢失
        部署时建议使用redis
        Returns:
            [type]: [{}]购物车数据
        """
        # 如果缓存在内存中，那么从缓存中读取购物车信息
        carts = cache.get(self.request.user.id)
        if carts:
            return carts
        else:
            return []
        
    def get_order_sn(self):
        # 生成订单号
        order_sn = timezone.now().strftime('%Y%m%d%H%M%S') + '%09d' % self.request.user.id
        return order_sn
    
    def get_sku_total_price(self, carts):
        """计算商品总金额，不含运费

        Args:
            carts (list): [购物车选中结算的数据列表]

        Returns:
            [float]: [商品总价金额，保留两位小数]
        """
        sku_total_price = [ Decimal(cart.get('sku__sell_price')) * cart.get('num') for cart in carts ]
        return sum(sku_total_price)
    
    def get_type(self):
        # 获取get请求中携带的类型
        cart = self.request.GET.get('type')
        return cart
        
    def del_stock(self, sku, num, time=DEL_STOCK_TIMING):
        # 减库存操作
        # time为0时加购减库存
        if time:
            sku.stocks = F('stocks') - int(num)
            sku.save()
            
                
                
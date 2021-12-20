import json
from django.core import serializers
from django.views.generic import DetailView
from DJMall.utils.views import DJMallBaseView
from product.models import category
from product.models.product import (
    DJMallProductSKU, DJMallProductSPU, DJMallProductCarouse, 
    DJMallProductSPUSpec, DJMallProductSPUSpecOption)


class ProductDetailView(DJMallBaseView, DetailView):
    """ 商品详情 """
    template_name = "product/product.html"
    queryset = DJMallProductSPU.objects.filter(is_del=False)
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_image'] = self.ge_slider_image()
        context['spec_json'] = self.get_spec_json()
        context['spec_sku_json'] = self.get_sku_json()
        context['current_options'] = self.get_current_sku()
        context['product_news'] = self.get_product_news()
        return context

    def get_product_dict(self):

        product_dict = {}
        # 1. 处理当前spu的数据，并包装包product_dict中
        spu_queryset = DJMallProductSPU.objects.filter(id=self.get_object().id)
        spu_json = serializers.serialize('json', spu_queryset)
        spu_list = json.loads(spu_json)
        for spu in spu_list:
            product_dict['storeInfo'] = spu.get('fields')

        # 2. 遍历出spu关联的轮播图
        product_dict['storeInfo']['slider_image'] = [ image.img.url for image in DJMallProductCarouse.objects.filter(spu=self.get_object()) ]

        # 3. 规格数据
        specs = serializers.serialize('json', self.get_object().djmallproductspuspec_set.all())
        specs = json.loads(specs)
        productAttr = []
        for spec in specs:
            productAttr.append(spec.get('fields'))
            options = DJMallProductSPUSpecOption.objects.filter(spec=spec.get('pk'))
            spec.get('fields')['attr_values'] = [ option.value for option in options ]

        product_dict['productAttr'] = productAttr

        # 4. spu下的sku关联数据
        # {'规格'：'sku'}前端匹配规格下的数据
        spec_sku_dict = {}
        sku_queryset = DJMallProductSKU.objects.filter(spu=self.get_object().id)

        for temp_sku in sku_queryset:
            temp_sku_queryset = temp_sku.options.values('value')
            values = [ temp_sku_option['value'] for temp_sku_option in temp_sku_queryset]
            options_str = ','.join(values)
            spec_sku_dict[options_str] = {
                'spu_id': temp_sku.spu.id,
                'sku_id': temp_sku.id,
                'sku_sell_price': '%.2f' % temp_sku.sell_price,
                'sku_image': f'/media/{temp_sku.main_picture}',
                'sku_bar_code': temp_sku.bar_code,
                'sku_market_price': '%.2f' % temp_sku.market_price,
                'sku_cost_price': '%.2f' % temp_sku.cost_price,
                'sku_sales': temp_sku.sales,
                'sku_stocks': temp_sku.stocks
            }
        
        product_dict['productValue'] = spec_sku_dict
        return product_dict

    def ge_slider_image(self):
        # 轮播图
        slider_image = self.get_product_dict()['storeInfo']['slider_image']
        slider_image.insert(0, '/{}'.format(self.get_product_dict()['storeInfo']['main_picture']))
        return json.dumps(slider_image, ensure_ascii=False)

    def get_spec_json(self):
        # 规格选项
        return json.dumps(self.get_product_dict()['productAttr'], ensure_ascii=False)

    def get_sku_json(self):
        # 规格对应的sku数据
        return json.dumps(self.get_product_dict()['productValue'], ensure_ascii=False)

    def get_current_sku(self):
        # 获取存在对应sku的规格值
        if self.get_product_dict()['productValue']:
            keys = self.get_product_dict()['productValue'].keys()
            key_list = None
            if list(keys)[0] == '':
                pass
            else:
                key_list = list(keys)[0].split(',')
                # [10斤装/礼盒, 70#]  
                return json.dumps(key_list, ensure_ascii=False)
    
    def get_product_news(self):
        # 新品推荐
        # [{'spu': 'sku'}, {'spu': 'sku'}]
        category = self.get_object().category.all().first()
        spu_queryset = DJMallProductSPU.objects.filter(category=category, is_new=True)[:5]
        product_list = []
        for spu in spu_queryset:
            prduct_dict = {}
            prduct_dict[spu] = spu.djmallproductsku_set.first()
            product_list.append(prduct_dict)
        return product_list
        
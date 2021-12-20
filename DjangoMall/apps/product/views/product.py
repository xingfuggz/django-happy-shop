import json
from django.core import serializers
from django.views.generic import DetailView
from DJMall.utils.views import DJMallBaseView
from product.models.product import DJMallProductSPU, DJMallProductSKU, DJMallProductCarouse, DJMallProductSPUSpecOption


class DJMallProductSPUDetailView(DJMallBaseView, DetailView):
    """ 商品详情 """
    template_name = 'product/product_detail.html'
    queryset = DJMallProductSPU.objects.filter(is_del=False)
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['product_dict'] = self.get_product_dict()
        context['slider_image'] = self.get_slider_image()
        context['spec_json'] = self.get_spec_json()
        context['spec_sku_json'] = self.get_sku_json()
        context['product_news'] = self.get_product_news()
        context['current_sku'] = self.get_current_sku()
        return context

    def get_product_dict(self):
        product_dict = {}

        # 1. 处理当前的spu数据，并包装到product_dict
        product = DJMallProductSPU.objects.filter(id=self.get_object().id)
        # print(product)
        # 序列化当前spu数据
        from django.core import serializers
        spu = serializers.serialize('json', product)
        spu = json.loads(spu)
        for stor in spu:
            product_dict['storeInfo'] = stor.get('fields')
            product_dict['storeInfo']['main_picture'] = '/{}'.format(product_dict['storeInfo']['main_picture'])
        # print(product_dict)

        # 2. 遍历出spu关联的轮播图
        product_dict['storeInfo']['slider_image'] = [image.img.url for image in DJMallProductCarouse.objects.filter(spu=self.get_object())]
        # 拼接补全图片路径
        # for i, img in enumerate(product_dict['storeInfo']['slider_image']):
        #     product_dict['storeInfo']['slider_image'][i] = f'/media{img}'
        # print(product_dict)

        # 3. 规格数据
        specs = serializers.serialize('json', self.get_object().djmallproductspuspec_set.all())
        specs = json.loads(specs)
        productAttr = []
        for spec in specs:
            productAttr.append(spec.get('fields', None))
            # 获取当前spec下的所有的option
            options = DJMallProductSPUSpecOption.objects.filter(spec=spec.get('pk'))
            spec.get('fields', None)['attr_values'] = [ option.value  for option in options] 
            # print(options)
        product_dict['productAttr'] = productAttr

        # 4. spu下的sku关联数据
        spec_sku_dict = {}
        sku_queryset = DJMallProductSKU.objects.filter(spu=self.get_object().id)
        # temp_sku_queryset = None
        for temp_sku in sku_queryset:
            temp_sku_queryset = temp_sku.options.values('value')
            # print(temp_sku_queryset)
            # option_str = None
            values = [temp_sku_option['value'] for temp_sku_option in temp_sku_queryset]
            options_str = ','.join(values)
            spec_sku_dict[options_str] = {
                'spu_id': temp_sku.spu.id,
                'sku_id': temp_sku.id, 
                'sku_sell_price': '%.2f' % temp_sku.sell_price, 
                'sku_image': f'/media/{temp_sku.main_picture}',
                'sku_bar_code': temp_sku.bar_code,
                'sku_market_price': '%.2f' % temp_sku.market_price,
                'sku_cost_price': '%.2f' % temp_sku.cost_price,
                # 'sku_product_unit': temp_sku.product_unit,
                'sku_sales': temp_sku.sales,
                'sku_stocks': temp_sku.stocks
            }
        product_dict['productValue'] = spec_sku_dict
        return product_dict

    def get_product_json(self):
        # product的json数据
        return json.dumps(self.get_product_dict(), ensure_ascii=False)
    
    def get_slider_image(self):
        # 轮播图的json数据
        slider_image = self.get_product_dict()['storeInfo']['slider_image']
        slider_image.insert(0, self.get_product_dict()['storeInfo']['main_picture'])
        return json.dumps(slider_image, ensure_ascii=False)

    def get_spec_json(self):
        # 规格的json数据
        return json.dumps(self.get_product_dict()['productAttr'], ensure_ascii=False)
    
    def get_sku_json(self):
        # sku的具体数据        
        return json.dumps(self.get_product_dict()['productValue'], ensure_ascii=False)
    
    def get_product_news(self):
        # 新品推荐
        category = self.get_object().category.all().first()
        spu_queryset = DJMallProductSPU.objects.filter(category=category, is_new=True)
        product_list = []
        for spu in spu_queryset:
            product_dict = {}
            product_dict[spu] = spu.djmallproductsku_set.first()
            product_list.append(product_dict)
        return product_list

    def get_current_sku(self):
        # 获取存在值得options
        if self.get_product_dict()['productValue']:
            keys = self.get_product_dict()['productValue'].keys()
            key_list = None
            if list(keys)[0] == '':
                pass
            else:
                key_list = list(keys)[0].split(',')  
            return json.dumps(key_list, ensure_ascii=False) 

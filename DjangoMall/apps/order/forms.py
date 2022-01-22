from django import forms
from django.forms import ModelForm
from django.core.cache import cache
from order.models import DJMallOrderInfo, DJMallOrderProduct
from users.models import DJMallAddress


class DJMallOrderInfoForm(ModelForm):
    # 订单表单
    # address = forms.ModelMultipleChoiceField(queryset=None, widget=forms.Select)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self)
        # self.fields['address'].queryset = DJMallAddress.objects.all()
    
    class Meta:
        model = DJMallOrderInfo
        fields = ['owner', 'pay_method', 'order_mark', 'address',]

    
class DJMallOrderProductForm(ModelForm):
    
    # sku = forms.ModelMultipleChoiceField(queryset=None, widget=forms.Select)
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['sku'].queryset = DJMallOrderProduct.objects.all()
    
    # 订单商品表单
    class Meta:
        model = DJMallOrderProduct
        fields = ['order', 'sku',]
        
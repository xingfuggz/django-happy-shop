from django import forms
from django.forms import ModelForm
from django.core.cache import cache
from order.models import DJMallOrderInfo, DJMallOrderProduct
from users.models import DJMallAddress


class DJMallOrderInfoForm(ModelForm):
    # 订单表单
    # address_data = forms.ModelMultipleChoiceField(queryset=None, widget=forms.Select)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # self.fields['address_data'].queryset = DJMallAddress.objects.filter(owner=user)
        # print()
    
    class Meta:
        model = DJMallOrderInfo
        fields = ['pay_method', 'order_mark', 'address',]

    
class DJMallOrderProductForm(ModelForm):
    
    # sku = forms.ModelMultipleChoiceField(queryset=None, widget=forms.Select)
    
    def __init__(self, *args, **kwargs):
        # print(kwargs)
        super().__init__(*args, **kwargs)
        # self.fields['sku'].queryset = D.objects.all()
        print(kwargs)
    
    # 订单商品表单
    class Meta:
        model = DJMallOrderProduct
        fields = ['order', 'sku',]
        
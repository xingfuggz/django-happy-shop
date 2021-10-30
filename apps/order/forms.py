from django import forms
# from django.forms import fields
from order.models import DmallShopingCart, DmallOrderInfo
# from django.core.exceptions import ValidationError


class DmallCartForm(forms.ModelForm):
    """Form definition for DmallCart."""
    owner = forms.HiddenInput()

    class Meta:
        """Meta definition for DmallCartform."""

        model = DmallShopingCart
        fields = ('owner', 'sku', 'num')

    def clean(self):
        data = self.cleaned_data
        if DmallShopingCart.objects.filter(sku=data['sku']).first():
            raise forms.ValidationError('yicunzai ')
        return self.cleaned_data


class DmallOrderInfoForm(forms.ModelForm):
    # 订单生成
    
    class Meta:
        model = DmallOrderInfo
        fields = ('pay_method', 'order_mark', 'address',)
        
    def clean_address(self):
        address = self.cleaned_data['address']
        if not address:
            raise forms.ValidationError('用户名与密码不能相同！')
        return address
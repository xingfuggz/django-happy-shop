from django import forms
from django.contrib.auth import get_user_model


class DJMallRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="再次输入密码", max_length=32, required=True)
    code = forms.CharField(label="请输入验证码", max_length=4, required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['password', 'email']


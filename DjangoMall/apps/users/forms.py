from datetime import timedelta
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField, CaptchaTextInput

from users.models import DJMallUser, DJMallEmailVerifyRecord


class DJMallRegisterForm(forms.ModelForm):
    # 注册表单
    password1 = forms.CharField(label="再次输入密码", max_length=32, required=True)
    code = forms.CharField(label="请输入验证码", max_length=4, required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['password', 'username']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

    def clean_password1(self):
        """验证密码是否相等"""
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('两次密码输入不一致！')
        return self.cleaned_data['password1']
    
    def clean_username(self):
        # 验证邮箱地址
        user = DJMallUser.objects.filter(email=self.cleaned_data['username']).exists()
        if user:
            raise forms.ValidationError('该用户已经存在！')
        return self.cleaned_data['username']
    
    def clean_code(self):
        # 验证码过期判断
        code = DJMallEmailVerifyRecord.objects.filter(code=self.cleaned_data['code'])
        if code.exists():
            code = code.last()
            intervals_time = timezone.now() - code.add_date
            if intervals_time > timedelta(hours=0, minutes=5, seconds=0):
                raise forms.ValidationError('该验证码已过期！')
        else:
            raise forms.ValidationError('无效验证码！')
        return self.cleaned_data['code']
    

class DJMallLoginCaptchaTextInput(CaptchaTextInput):
    # 登录表单组件样式重写
    template_name = "users/login_captcha.html"


class DJMallLoginAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(widget=DJMallLoginCaptchaTextInput(attrs={'placeholder': '请输入验证码'}))

    class Media:
        js = ['admin/js/vendor/jquery/jquery.js',]
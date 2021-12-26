from django import forms
from django.contrib.auth import get_user_model
from django.http.response import Http404, HttpResponse, JsonResponse
from users.models import DJMallEmailVerifyRecord


class DJMallUserEmailForm(forms.ModelForm):
    # 邮件验证
    code = forms.CharField(label="验证码", max_length=4, error_messages={'required':'验证码不能为空！'})
    
    class Meta:
        model = get_user_model()
        fields = ['email']
        
    def clean_code(self):
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('该邮箱地址已被使用，请更换其他邮箱！')
        elif self.cleaned_data['code'] == '':
            raise forms.ValidationError('验证码不能为空！')
        return self.cleaned_data['code']
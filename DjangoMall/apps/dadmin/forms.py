from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField, CaptchaTextInput


class DJMallCaptchaTextInput(CaptchaTextInput):
    template_name = "dadmin/captcha.html"


class DJMallAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(widget=DJMallCaptchaTextInput(attrs={'placeholder': '请输入验证码'}))

    class Media:
        js = ['admin/js/vendor/jquery/jquery.js',]
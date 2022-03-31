from django import forms
from django.contrib.auth.password_validation import password_changed
from django.forms import TextInput, PasswordInput, ValidationError
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class HappyShopTextInput(TextInput):
    input_type = "text"
    template_name = "happy_shop/widgets/text.html"


class HappyShopPasswordInput(PasswordInput):
    input_type = "password"
    template_name = "happy_shop/widgets/text.html"


class HappyShopLoginForm(AuthenticationForm):
    """ 登录表单 """
    username = UsernameField(widget=HappyShopTextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=HappyShopPasswordInput(attrs={"autocomplete": "current-password"}),
    )


class HappyShopRegisterForm(forms.ModelForm):
    """ 注册视图 """
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    username = forms.CharField(label="用户名", required=True, widget=HappyShopTextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="密码",
        strip=False,
        widget=HappyShopPasswordInput(attrs={"autocomplete": "current-password"}),
    )
    password1 = forms.CharField(
        label=_("再输入一次密码"),
        strip=False,
        widget=HappyShopPasswordInput(attrs={"autocomplete": "current-password"}),
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise ValidationError( 
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password1

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_obj = User.objects.filter(username=username)
        if user_obj.exists():
            raise ValidationError("该用户名已经存在，请更换用户名！")
        return username
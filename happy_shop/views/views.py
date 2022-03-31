from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from happy_shop.models import HappyShopingCart
from happy_shop.conf import happy_shop_settings
# Create your views here.
from happy_shop.forms import HappyShopLoginForm, HappyShopRegisterForm


class BaseView:
    """全局基类视图"""
    
    title = happy_shop_settings.TITLE
    desc = happy_shop_settings.DESC
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['desc'] = self.desc
        if self.request.user.is_authenticated:
            context['cart_num'] = HappyShopingCart.get_cart_count(self.request.user)
        else:
            context['cart_num'] = 0
        return context


class HappyShopLoginView(BaseView, LoginView):
    """
    登录视图
    """
    form_class = HappyShopLoginForm
    template_name = "happy_shop/login.html"
    next_page = "happy_shop:index"
    extra_context = {
        "site_title": "登录",
    }


class HappyShopRegisterView(BaseView, FormView):
    """
    注册用户 
    """
    template_name = 'happy_shop/register.html'
    form_class = HappyShopRegisterForm
    success_url = reverse_lazy("happy_shop:index")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data.get('password'))
        new_user.username = form.cleaned_data.get('username')
        new_user.save()
        return super().form_valid(form)


class HappyShopLogoutView(BaseView, LogoutView):
    """
    Log out the user and display the 'You are logged out' message.
    """

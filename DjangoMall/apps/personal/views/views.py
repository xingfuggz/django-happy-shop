from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
# Create your views here.
from DJMall.utils.views import DJMallBaseView
from personal.forms import DJMallUserEmailForm


class DJMallLoginRequiredMixin(LoginRequiredMixin):
    # 登录权限
    login_url = '/users/login/'
    redirect_field_name = 'redirect_to'


class DJMallUserPersonalView(DJMallLoginRequiredMixin, DJMallBaseView, TemplateView):
    """用户中心首页

    Args:
        DJMallLoginRequiredMixin ([type]): [description]
        DJMallBaseView ([type]): [description]
        TemplateView ([type]): [description]
    """
    template_name = 'personal/index.html'
    

class DJMallUserUpdateView(DJMallLoginRequiredMixin, DJMallBaseView, UpdateView):
    # 修改用户名
    model = get_user_model()
    fields = ['username']
    template_name = 'personal/update_username.html'
    success_url = '/personal/home/'
    
    
class DJMallUserUpdateEmailView(DJMallUserUpdateView):
    # 修改邮箱号
    model = get_user_model()
    form_class = DJMallUserEmailForm
    fields = None
    template_name = 'personal/update_email.html'
    success_url = '/personal/home/'
    
    
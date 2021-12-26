from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model

# Create your views here.
from DJMall.utils.views import DJMallBaseView
from users.forms import DJMallLoginAuthenticationForm
from users.forms import DJMallRegisterForm

User = get_user_model()


class DJMallAuthBackend(ModelBackend):
    """ 自定义用户验证，继承ModelBackend, 重写authenticate方法
    ModelBackend 类实际是django继承BaseBackend实现的验证登录后端，
    我们这里使用的是django自带的验证后端，那最好的做法就是扩展重写该类
    """
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class DJMallLoginView(DJMallBaseView, LoginView):
    # 登录页面
    form_class = DJMallLoginAuthenticationForm
    template_name = 'users/login.html'
    success_url = '/'
    extra_context = {
        'title': '登录',
        'sub_title': 'DJMall商城系统！'
    }
    
    def get_success_url(self) -> str:
        if self.request.GET['redirect_to']:
            self.success_url = self.request.GET['redirect_to']
            return self.success_url
        return super().get_success_url()

class DJMallRegisterView(DJMallBaseView, CreateView):
    # 注册视图
    template_name = 'users/register.html'
    form_class = DJMallRegisterForm
    success_url = "/users/login/"


class DJMallLogoutView(LogoutView):
    # 退出登录
    template_name = 'users/logout.html'
    redirect_authenticated_user = True
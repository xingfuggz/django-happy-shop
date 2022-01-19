from datetime import timedelta
from django.http.response import JsonResponse
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.utils import timezone
from DJMall.utils.views import JsonableResponseMixin
from users.models import DJMallEmailVerifyRecord
from DJMall.utils.utils import random_str, send_email

User = get_user_model()


class DJMallEmailVerifyRecordCreateView(JsonableResponseMixin, CreateView):
    model = DJMallEmailVerifyRecord
    fields = ['email', 'send_type']
    template_name = 'users/code.html'
    
    def form_valid(self, form):
        code = random_str()
        form.instance.code = code
        email = form.cleaned_data['email']
        # 验证邮箱是否已经被注册
        if self.verify_email(email).exists():
            return JsonResponse({'code': 412, 'message': '该邮箱已被注册，请更换邮箱！'})
        
        # 验证发送频率
        intervals_time = timezone.now() - timedelta(hours=0, minutes=1, seconds=0)
        if DJMallEmailVerifyRecord.objects.filter(add_date__gt=intervals_time, email=email):
            return JsonResponse({'code': 412, 'message': '时间间隔小于60s，请60s后重新获取！'})
        # 验证码保存到数据库
        form.save()
        
        # 发送邮件
        send_email(subject="DJMall商城注册验证码，请查收！", message=f'您的注册邮箱验证码是：{code},5分钟内有效！', to_emial=[email])
        return JsonResponse({'code': 200, 'message': '验证码已发送，请登录邮箱查收！'})
    
    def get_email_code(self):
        # 查询数据库最新的code
        return DJMallEmailVerifyRecord.objects.last()
        
    def verify_email(self, email):
        # 验证用户是否存在
        # @params email 用户表单提交的邮箱
        # @return True or False
        return User.objects.filter(email=email)
            
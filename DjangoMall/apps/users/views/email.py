from django.http.response import JsonResponse
from django.views.generic import CreateView
from DJMall.utils.views import JsonableResponseMixin
from users.models import DJMallEmailVerifyRecord
from DJMall.utils.utils import random_str, send_email


class DJMallEmailVerifyRecordCreateView(JsonableResponseMixin, CreateView):
    model = DJMallEmailVerifyRecord
    fields = ['code', 'email', 'send_type']
    template_name = 'users/code.html'
    
    def form_valid(self, form):
        code = random_str()
        email = form.cleaned_data['email']
        send_email(subject="DJMall商城注册验证码，请查收！", message=f'您的注册邮箱验证码是：{code}', to_emial=[email])
        # form.save()
        
        email_code = self.get_email_code().code
        form_code = form.cleaned_data['code']
        # print(form_code, email_code)
        if not form_code or form_code.lower() != email_code.lower():
            print('请正确填写验证码')
            form.instance.code = form.cleaned_data['code']  # 设置验证码
        else:
            print('zhengque')
        
        
        return JsonResponse({'code': 'ok'})
    
    def get_email_code(self):
        # 验证code值
        return DJMallEmailVerifyRecord.objects.all().last()
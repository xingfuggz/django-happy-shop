# django-happy-shop

#### 介绍
一个可以快速集成到任何django项目的商城模块，正如他的名字一样，简单、快乐，使用愉快！

#### 软件架构
HappyShop 是一个 Django 开发的第三方包，用于快速集成到任何django项目，以便快速获得一个简单的商城功能。

本项目采用django + DRF + vue开发，具备前后端分离基因，拥有完整的多规格商品逻辑，集成支付宝支付，只需要简单配置即可快速收款！

其他功能还在迭代中...


#### 安装教程

1. 使用 pip 命令快速安装
```
pip3 install django-happy-shop
```
#### 使用说明

2. 将 "happy_shop" 添加到您的 INSTALLED_APPS 设置中，以及项目需要的其他几个依赖，如下所示：
```
    INSTALLED_APPS = [
        ...
        'happy_shop',      # happy_shop主程序
        'rest_framework',   # DRF
        'corsheaders',      # 处理跨域的包
        'crispy_forms',     # 可浏览API的form包，便于调试
    ]
```
3. 在项目 urls.py 中包含 happy_shop 的 URLconf，如下所示
```
from rest_framework.documentation import include_docs_urls

# 这里url开头的happy请不要自定义，可能会影响某些接口的运作    
path('happy/', include('happy_shop.urls')),   
           
# 需要查看drf的接口文档请配置
path('docs/', include_docs_urls(title='HappyShop API')), 
# 需要DRF的可浏览API能力请配置 
path('api-auth/', include('rest_framework.urls')),    
```
4. 运行 ``python manage.py migrate`` 创建simple_shop的模型数据.

5. 运行 ``python manage.py runserver`` 启动开发服务器

6. 访问 http://127.0.0.1:8000/happy/ 访问该商城系统.

7. 当前商城系统后台依赖django默认的admin，请访问`http://127.0.0.1:8000/admin/`
进入后台进行数据管理，请自行创建管理员账号密码及无比开启django管理后端【django默认后端】！

8. 支付宝支付配置，需要在项目中的settings文件中自行配置，默认加密方式为RSA2，如下所示：
```    
    HAPPY_SHOP = {
        'ALIPAY':{
            'APPID': appid
            'RETURN_URL': 'http://127.0.0.1:8000/happy/api/alipay/',
            'NOTIFY_URL': 'http://127.0.0.1:8000/happy/api/alipay/',
            'DEBUG': DEBUG, 
            'PRIVATE_KEY':BASE_DIR / 'app_private_key.pem',    # 应用私钥
            'PUBLIC_KEY':BASE_DIR / 'alipay_public_key.pem',   # 支付宝公钥，不是应用公钥
        },
    }
```   
私钥与公钥一定要配置正确，否则回调无法验证成功，订单状态无法修改！
部署时一定要关闭django的DEBUG模式，否则支付地址跳转为沙箱地址，不能正确收款！


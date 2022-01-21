from .base import *
from config.cache import dummy, redis

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATICFILES_DIRS = [
    BASE_DIR / f'themes/{TEMPLATE_NAME}/static'
]

MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'static'

# 虚拟缓存
# CACHES = dummy

EMAIL_HOST = 'smtp.qq.com'   # 用于发送电子邮件的主机。
EMAIL_HOST_USER = "1158920674@qq.com"    # 自己的邮箱地址
EMAIL_HOST_PASSWORD = "hfswjziyvgcqjiaa"       # 自己的邮箱密码
EMAIL_PORT = 465                     # 用于中定义的SMTP服务器的端口
EMAIL_USE_SSL = True             # 是否使用隐式的安全连接

# 开发阶段的邮件端
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
from pathlib import Path
from django.conf import settings

BASE_DIR = BASE_DIR = Path(__file__).resolve().parent.parent

alipay_private_key = BASE_DIR / 'pay/alipay/keys/app_private_key.pem'
alipay_public_key = BASE_DIR / 'pay/alipay/keys/app_public_key.pem'

DEFAULTS = {
    'TITLE': 'HappyShop',
    'DESC': 'HappyShop是一个非常简单和便于使用的商城系统，采用Python的django框架开发！',

    # 支付宝支付的key文件路径
    'ALIPAY':{
        'APPID': '2021000116697536',
        'RETURN_URL': 'http://127.0.0.1:8000/shop/api/alipay/',
        'NOTIFY_URL': 'http://127.0.0.1:8000/shop/api/alipay/',
        'DEBUG': settings.DEBUG,           # 开发模式默认为True，部署时设置为False
        'PRIVATE_KEY':alipay_private_key,
        'PUBLIC_KEY':alipay_public_key,
    },

    # 首页楼层商品显示数量
    'FLOOR_NUM': 8, 
    
    # 商品列表页分页
    'PAGE_SIZE': 20,       # 每页商品数量
    'MAX_PAGE_SIZE': 100,  # 最大分页数

    # 商品详情页新品推荐数量
    'NEW_NUM': 5,
    
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # ],
}

# 可能采用字符串导入表示法的设置列表。
IMPORT_STRINGS = [
    'DEFAULT_RENDERER_CLASSES',
]

# 已删除的设置列表
REMOVED_SETTINGS = [
    'PAGINATE_BY', 'PAGINATE_BY_PARAM', 'MAX_PAGINATE_BY',
]

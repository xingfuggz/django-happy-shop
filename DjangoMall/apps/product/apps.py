from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
    verbose_name = '商品'
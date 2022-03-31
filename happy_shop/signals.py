from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HappyShopOrderSKU


@receiver(post_save, sender=HappyShopOrderSKU)
def create_ordersku(sender, instance=None, created=False, **kwargs):
    # 用户注册时自动将密码转为密文
    if created:
        instance.sku.stocks -= instance.count
        instance.sku.sales += instance.count
        instance.sku.save()
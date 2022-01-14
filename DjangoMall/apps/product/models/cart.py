from django.db import models
from django.contrib.auth import get_user_model
from DJMall.utils.models import DJMallBaseModel
from product.models import DJMallProductSKU

User = get_user_model()


class DJMallShopingCart(DJMallBaseModel):
    # 购物车数据模型
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    sku = models.ForeignKey(DJMallProductSKU, on_delete=models.CASCADE, verbose_name="商品sku")
    num = models.PositiveIntegerField(default=1, verbose_name="数量")
    
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['owner', 'sku'], name='unique_owner_sku')
        ]
        
    def __str__(self):
        return f'{self.owner}{self.sku}'
    
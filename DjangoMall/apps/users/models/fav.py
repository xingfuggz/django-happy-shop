from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from DJMall.utils.models import DJMallBaseModel

User = get_user_model()


class DJMallFavorite(DJMallBaseModel):
    """通用收藏模型
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关联用户")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ("owner", "content_type", "object_id")
        
    def __str__(self):
        return f'{self.object_id}{self.content_object}'
    
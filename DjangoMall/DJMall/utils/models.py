from django.db import models


class DJMallBaseModel(models.Model):
    """ 
    全局继承基类
    """
    add_date = models.DateTimeField("添加时间", auto_now_add=True)
    pub_date = models.DateTimeField("修改时间", auto_now=True)
    is_del = models.BooleanField(default=False)

    class Meta:
        abstract = True
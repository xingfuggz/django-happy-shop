'''
@file            :config.py
@Description     :配置文件
@Date            :2021/12/22 12:56:34
@Author          :幸福关中 && 轻编程
@version         :v1.0
@GiteeUrl        :https://gitee.com/xingfugz/django-mall
'''

#####                         虚拟缓存后端【用于开发模式】                           #####
# https://docs.djangoproject.com/zh-hans/4.0/topics/cache/#dummy-caching-for-development
#--------------------------------------------------------------------------------------#
dummy = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
#--------------------------------------------------------------------------------------#


#####                                   Redis缓存后端                                #####
# https://docs.djangoproject.com/zh-hans/4.0/topics/cache/#redis
#----------------------------------------------------------------------------------------#
redis = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://username:password@127.0.0.1:6379',
    }
}
#----------------------------------------------------------------------------------------#
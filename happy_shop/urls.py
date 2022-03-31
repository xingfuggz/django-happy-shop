from rest_framework.documentation import include_docs_urls
from django.urls import path, include
from .import views

app_name = "happy_shop"

urlpatterns = [
    path('api/', include('happy_shop.api.api_urls')),
    path('docs/', include_docs_urls(title='HappyShop API')),
    path('api-auth/', include('rest_framework.urls')),
    
    # PC端
    path("", views.IndexView.as_view(), name="index"),
    path("goods/<int:pk>/", views.HappyShopCategoryView.as_view(), name="goods"),
    path("goods/<int:pk>/detail/", views.HappyShopSPUDetailView.as_view(), name="goods_detail"),
    path("cart/", views.HappyShopingCartView.as_view(), name="cart"),
    path("pay/", views.HappyShopPayView.as_view(), name="pay"),
    path('user_profile/', views.HappyShopUserProfileView.as_view(), name='user_profile'),
    path('user_orders/', views.HappyShopUserOrdersView.as_view(), name='user_orders'),
    path('user_orders/<int:pk>/', views.HappyShopUserOrdersDetailView.as_view(), name='user_orders_detail'),
    path('user_address/', views.HappyShopUserAddressView.as_view(), name='user_address'),
    path("login/", views.HappyShopLoginView.as_view(), name="login"),
    path("register/", views.HappyShopRegisterView.as_view(), name="register"),
    path('logout/', views.HappyShopLogoutView.as_view(), name='logout'),
]


# 支付宝支付的回调URL
from rest_framework.urlpatterns import format_suffix_patterns
from happy_shop.api.views import AliPayView

api_urlpatterns = [
    path('api/alipay/', AliPayView.as_view(), name="alipay"),
]

urlpatterns += format_suffix_patterns(api_urlpatterns)

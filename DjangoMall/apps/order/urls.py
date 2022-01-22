from django.urls import path, re_path
from .import views

app_name = 'order'

urlpatterns = [
    path("pay/", views.DJMallPayView.as_view(), name="pay"),
    path("orderinfo/", views.DJMallOrderInfoView.as_view(), name="orderinfo")
]
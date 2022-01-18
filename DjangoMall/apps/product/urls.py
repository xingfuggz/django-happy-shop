from django.urls import path

from .import views

app_name = "product"

urlpatterns = [
    path('category_list/', views.DJMallProductCategoryListView.as_view(), name="category_list"),
    path('category/<int:pk>/', views.DJMallProductCategoryView.as_view(), name="category_detail"),
    path('goods/<int:product_id>/detail/', views.ProductDetailView.as_view(), name="product_goods_detail"),
    path("cart/", views.DJMallShopingCartView.as_view(), name="cart"),
    path("cart/del/<int:pk>/", views.DJMallShopingCartDeleteView.as_view(), name="cart_delete")
]
from django.urls import path, re_path
from .import views

app_name = 'personal'

urlpatterns = [
    path("home/", views.DJMallUserPersonalView.as_view(), name="home"),
    path("username/<int:pk>/update/", views.DJMallUserUpdateView.as_view(), name="update_username"),
    path("email/<int:pk>/update/", views.DJMallUserUpdateEmailView.as_view(), name="update_email"),
    path('fav_list/', views.DJMallFavoriteListView.as_view(), name='fav_list'),
    path("fav_delete/<int:pk>/", views.DJMallFavoriteDeleteView.as_view(), name="fav_delete"),
    path("address/list/", views.DJMallAddressListView.as_view(), name="address_list"),
    path("address/create/", views.DJMallAddressCreateView.as_view(), name="address_create"),
]

from django.urls import path, re_path
from .import views

app_name = 'personal'

urlpatterns = [
    path("home/", views.DJMallUserPersonalView.as_view(), name="home"),
    path("username/<int:pk>/update/", views.DJMallUserUpdateView.as_view(), name="update_username"),
    path("email/<int:pk>/update/", views.DJMallUserUpdateEmailView.as_view(), name="update_email"),
    path('fav_list/', views.DJMallFavoriteListView.as_view(), name='fav_list'),
]

from django.urls import path, re_path
from .views import DJMallUserPersonalView, DJMallUserUpdateView, DJMallUserUpdateEmailView

app_name = 'personal'

urlpatterns = [
    path("home/", DJMallUserPersonalView.as_view(), name="home"),
    path("username/<int:pk>/update/", DJMallUserUpdateView.as_view(), name="update_username"),
    path("email/<int:pk>/update/", DJMallUserUpdateEmailView.as_view(), name="update_email"),
]

from django.urls import path, include
from .import views

app_name = 'users'

urlpatterns = [
    path("login/", views.DJMallLoginView.as_view(), name="login"),
    path("register/", views.DJMallRegisterView.as_view(), name="register"),
]

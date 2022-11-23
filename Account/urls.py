from django.urls import path

from . import views

urlpatterns = [
    path("register", views.RegisterAPI.as_view(), name="index"),
    path("login", views.LoginAPI.as_view(), name="login"),
    path("token", views.TokenAPI.as_view(), name = "token")
]

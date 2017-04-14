# coding=utf8
from django.conf.urls import url
from authentication import views

urlpatterns = [
    url(r"^login/", views.LoginView.as_view(), name="login"),
    url(r"^logout/", views.logout, name="logout"),

    url(r"api/get-public", views.api_get_public_key, name="get_public"),
    url(r"api/login", views.api_login, name="api-login"),
]

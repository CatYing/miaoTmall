# coding=utf8
from django.conf.urls import url
from authentication import views

urlpatterns = [
    url(r"^login/", views.LoginView.as_view(), name="login"),
    url(r"^logout/", views.logout, name="logout"),
]

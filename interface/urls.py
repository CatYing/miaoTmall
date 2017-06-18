# coding=utf8
from django.conf.urls import url
from interface import views

urlpatterns = [
    url(r'send/', views.send, name='send'),
]
from django.conf.urls import url
from order import views

urlpatterns = [
    url("list/", views.list, name='order'),
    url("single/(?P<pk>[0-9]+)", views.single_item_cal, name='single-cal'),
]

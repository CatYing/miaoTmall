from django.conf.urls import url
from order import views

urlpatterns = [
    url("list/", views.order_list, name='order'),
    url("single/(?P<pk>[0-9]+)", views.single_item_cal, name='single-cal'),
    url("face/", views.face_pay, name='face'),
]

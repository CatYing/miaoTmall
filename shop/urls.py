from django.conf.urls import url
from shop import views

urlpatterns = [
    url(r"(?P<pk>[0-9]+)/", views.ShopDetailView.as_view(), name="shop-detail"),

]

from django.conf.urls import url
from shop import views

urlpatterns = [
    url(r"^self/", views.ShopSelfView.as_view(), name="self-shop"),
    url(r"^detail/(?P<pk>[0-9]+)/", views.ShopDetailView.as_view(), name="shop-detail"),
    url(r"^add", views.ItemCreateView.as_view(), name="add-item"),
    url(r"^edit/(?P<pk>[0-9]+)", views.ItemUpdateView.as_view(), name='edit-item'),

    url(r"^api/add", views.api_add_to_cart, name="add-cart"),
    url(r"api/remove", views.api_move_from_cart, name="remove-cart"),
]

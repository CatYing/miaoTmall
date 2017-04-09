from django.conf.urls import url
from verify import views

urlpatterns = [
    url(r"api/get-code", views.api_generate_code),
    url(r"api/verify-code", views.api_verify),
]

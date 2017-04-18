# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView
from website.mixin import FrontMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from shop.models import *
# Create your views here.


class ShopDetailView(FrontMixin, ListView):
    pass


class ItemCreateView(UserPassesTestMixin, FrontMixin, CreateView):
    template_name = "shop/add.html"
    model = Item
    fields = []

    def test_func(self):
        if self.request.user.myuser.current_stage >= 3:
            return True
        else:
            return False



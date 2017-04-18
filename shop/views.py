# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from website.mixin import FrontMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from shop.models import *

# Create your views here.


class ShopDetailView(FrontMixin, ListView):
    model = ItemCreateView
    context_object_name = 'item_list'
    template_name = 'shop/shop.html'



class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, FrontMixin, CreateView):
    template_name = "shop/add.html"
    model = Item
    fields = ['name', 'detail']
    login_url = reverse_lazy('login')
    success_url = reverse_lazy("shop")

    def test_func(self):
        return self.request.user.myuser.current_stage >= 3

    def form_valid(self, form):
        form.instance.prototype = Prototype.objects.get(pk=int(self.request.POST.get("prototype")))
        form.instance.myuser = self.request.user.myuser
        return super(ItemCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get(**kwargs)
        context['prototype_list'] = Prototype.objects.all()
        return context





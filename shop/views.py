# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from website.mixin import FrontMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from shop.models import *

# Create your views here.


class ShopDetailView(FrontMixin, ListView):
    model = ItemCreateView
    context_object_name = 'item_list'
    template_name = 'shop/shop.html'

    def get_queryset(self):
        return Item.objects.filter(myuser=MyUser.objects.get(pk=int(self.kwargs['pk'])))


class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, FrontMixin, CreateView):
    template_name = "shop/add.html"
    model = Item
    fields = ['name', 'detail']
    login_url = reverse_lazy('login')
    success_url = reverse_lazy("shop-detail")
    redirect_field_name = 'denied'

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


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, FrontMixin, UpdateView):
    login_url = reverse_lazy("login")
    model = Item
    context_object_name = 'info'
    fields = ['name', 'detail']
    template_name = 'shop/add.html'
    success_url = reverse_lazy("shop-detail")
    redirect_field_name = 'denied'

    def test_func(self):
        return self.request.user.myuser == Item.objects.get(pk=int(self.kwargs['pk'])).myuser

    def get_object(self, queryset=None):
        return Item.objects.get(pk=int(self.kwargs['pk']))


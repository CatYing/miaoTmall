# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from website.mixin import FrontMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from shop.models import *

# Create your views here.


class ShopDetailView(FrontMixin, ListView):
    model = Item
    context_object_name = 'item_list'
    template_name = 'shop/shop.html'

    def get_queryset(self):
        return Item.objects.filter(myuser=MyUser.objects.get(pk=int(self.kwargs['pk'])))

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(ShopDetailView, self).dispatch(request, *args, **kwargs)
        except:
            return render(request, 'error.html')

    def get_context_data(self, **kwargs):
        context = super(ShopDetailView, self).get_context_data(**kwargs)
        context['detail'] = MyUser.objects.get(pk=int(self.kwargs['pk']))
        return context


class ShopSelfView(LoginRequiredMixin, UserPassesTestMixin, FrontMixin, ListView):
    login_url = reverse_lazy("login")
    redirect_field_name = "denied"
    model = Item
    context_object_name = "item_list"
    template_name = 'shop/self.html'

    def test_func(self):
        return self.request.user.myuser.current_stage >= 3

    def get_queryset(self):
        return Item.objects.filter(myuser=self.request.user.myuser)


class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, FrontMixin, CreateView):
    template_name = "shop/add.html"
    model = Item
    fields = ['name', 'detail']
    login_url = reverse_lazy('login')
    success_url = reverse_lazy("self-shop")
    redirect_field_name = 'denied'

    def test_func(self):
        return self.request.user.myuser.current_stage >= 3

    def form_valid(self, form):
        form.instance.prototype = Prototype.objects.get(pk=int(self.request.POST.get("prototype")))
        form.instance.myuser = self.request.user.myuser
        return super(ItemCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['prototype_list'] = Prototype.objects.all()
        return context


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, FrontMixin, UpdateView):
    login_url = reverse_lazy("login")
    model = Item
    context_object_name = 'info'
    fields = ['name', 'detail']
    template_name = 'shop/add.html'
    success_url = reverse_lazy("self-shop")
    redirect_field_name = 'denied'

    def test_func(self):
        return self.request.user.myuser == Item.objects.get(pk=int(self.kwargs['pk'])).myuser

    def get_object(self, queryset=None):
        return Item.objects.get(pk=int(self.kwargs['pk']))


@login_required(login_url=reverse_lazy("login"))
def api_add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id", "").__int__()
        myuser_id = request.user.myuser.id
        item = Item.objects.get(id=item_id)
        if not item.locking_id:
            return HttpResponse(json.dumps({'result': '0', 'message': '已被锁定'}), content_type='application/json')
        else:
            item.locking_id = myuser_id
            item.save()
            return HttpResponse(json.dumps({'result': '1'}), content_type='application/json')
    else:
        pass


@login_required(login_url=reverse_lazy("login"))
def api_move_from_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id", "").__int__()
        myuser_id = request.user.myuser.id
        item = Item.objects.get(id=item_id)
        if item.locking_id != myuser_id:
            return HttpResponse(json.dumps({'result': '0', 'message': '您没有锁定该宠物'}), content_type=
                                'application/json')
        else:
            item.locking_id = 0
            item.save()
            return HttpResponse(json.dumps({'result': '1'}), content_type='application/json')


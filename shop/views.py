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

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        context['prototype_list'] = Prototype.objects.all()
        return context


class ShopListView(FrontMixin, ListView):
    template_name = 'shop/list.html'
    model = MyUser
    context_object_name = 'myuser_list'

    def get_queryset(self):
        return MyUser.objects.filter(level__gte=3)


class CartView(LoginRequiredMixin, FrontMixin, ListView):
    template_name = 'shop/cart.html'
    model = Item
    context_object_name = 'item_list'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Item.objects.filter(locking_id=self.request.user.myuser.id)


@login_required(login_url=reverse_lazy("login"))
def api_add_to_cart(request):
    if request.method == "POST":
        item_id = int(request.POST.get("item_id", ""))
        myuser_id = request.user.myuser.id
        item = Item.objects.get(id=item_id)
        if item.locking_id:
            return HttpResponse(json.dumps({'result': 0, 'message': '已被锁定'}), content_type='application/json')
        else:
            item.locking_id = myuser_id
            item.save()
            return HttpResponse(json.dumps({'result': 1}), content_type='application/json')
    else:
        pass


@login_required(login_url=reverse_lazy("login"))
def api_move_from_cart(request):
    if request.method == "POST":
        item_id = int(request.POST.get("item_id", ""))
        myuser_id = request.user.myuser.id
        item = Item.objects.get(id=item_id)
        if item.locking_id != myuser_id:
            return HttpResponse(json.dumps({'result': 0, 'message': '您没有锁定该宠物'}), content_type=
            'application/json')
        else:
            item.locking_id = 0
            item.save()
            return HttpResponse(json.dumps({'result': 1}), content_type='application/json')


@login_required(login_url=reverse_lazy("login"))
def api_unlock(request):
    if request.GET.get("item_id", ""):
        item_id = int(request.GET.get("item_id", ""))
        item = Item.objects.get(id=item_id)
        if item.myuser == request.user.myuser:
            item.locking_id = 0
            item.save()
            return HttpResponse(json.dumps({'result': 1}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'result': 0, 'message': '您无权解锁该宠物'}), content_type='application/json')


@login_required(login_url=reverse_lazy("login"))
def api_delete(request):
    if request.method == "POST":
        item_id = int(request.POST.get("item_id"))
        item = Item.objects.get(id=item_id)
        if item.myuser == request.user.myuser:
            item.delete()
            return HttpResponse(json.dumps({'result': 1}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'result': 0, 'message': '你无法删除该宠物'}), content_type='application/json')

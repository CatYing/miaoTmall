# -*- coding: utf-8 -*-
from order.models import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
import datetime


# Create your views here.


@login_required(login_url=reverse_lazy('login'))
def single_item_cal(request, pk):
    myuser = request.user.myuser
    item_id = int(pk)
    item = Item.objects.get(pk=item_id)
    if item.locking_id or not item.available:
        return render(request, 'error.html')
    else:
        new_order = Order(
            buyer_id=request.user.myuser.id,
            datetime=datetime.datetime.now(),
            price=item.price,
            state=0
        )
        new_order.save()
        new_order_item = OrderItem(
            order=new_order,
            item=item
        )
        new_order_item.save()
        content = {
            'order': new_order,
            'order_item': new_order_item,
            'seller': item.myuser,
            'myuser': myuser,
        }
        item.available = False
        item.save()
        return render(request, 'order/single.html', content)


@login_required(login_url=reverse_lazy('login'))
def cart_item_cal(request):
    myuser = request.user.myuser
    item_set = Item.objects.filter(locking_id=myuser.id)
    seller_existed = []
    for item in item_set:
        if item.myuser in seller_existed:
            pass


@login_required(login_url=reverse_lazy('login'))
def order_list(request):
    myuser = request.user.myuser
    order_list = Order.objects.filter(buyer_id=myuser.id)
    content = {
        'order_list': order_list,
        'myuser': myuser
    }
    return render(request, 'order/list.html', content)

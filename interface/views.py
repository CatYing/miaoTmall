# -*- coding: utf-8 -*-
from django.shortcuts import render
import json
import random
import rsa
from tmall.settings import BANK_HOST
from order.models import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


# Create your views here.


# 封装订单信息，验证通过后跳转
@login_required(login_url=reverse_lazy('login'))
def send(request):
    order_id = request.GET.get('id')
    order = Order.objects.filter(id=int(order_id))
    if order.count() == 0:
        return render(request, 'error.html')
    else:
        order = order[0]
        if order.buyer_id != request.user.myuser.id:
            return render(request, 'error.html')
        else:
            if order.orderitem_set[0].item.myuser.id == request.user.myuser.id:
                return render(request, 'error.html')
            else:
                message = {
                    'seller': order.orderitem_set[0].item.myuser.id,
                    'buyer': request.user.myuser.id
                }
                # 发送




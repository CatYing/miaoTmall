# -*- coding: utf-8 -*-
from django.http import HttpResponse

from order.models import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
import datetime
import requests
import json
from tmall.settings import API_KEY, API_SECRET


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


@login_required(login_url=reverse_lazy('login'))
def face_pay(request):
    myuser = request.user.myuser
    if request.method == 'GET':
        order_id = int(request.GET.get('order_id', ''))
        order = Order.objects.get(id=order_id)
        if order.buyer_id != myuser.id:
            return HttpResponse("非法用户")
        else:
            content = {
                'myuser': myuser
            }
            return render(request, 'order/facepay.html', content)
    else:
        face_token1 = myuser.face_token
        image_base64_2 = request.POST.get('snapShot')[22:]
        req = requests.post(
            url='https://api-cn.faceplusplus.com/facepp/v3/compare',
            data={
                'api_key': API_KEY,
                'api_secret': API_SECRET,
                'face_token1': face_token1,
                'image_base64_2': image_base64_2
            }
        )
        response = req.json()

        if response.has_key('error_message'):
            return HttpResponse(json.dumps({'error': True, 'data': "再试一次"}), content_type='application/json')
        else:
            if response.has_key('confidence'):
                if float(response.get("confidence")) >= 0.75:
                    order_id = int(request.GET.get('order_id', ''))
                    order = Order.objects.get(id=order_id)
                    order.state = 1
                    order.save()

                    return HttpResponse(json.dumps({'data': "支付成功"}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'error': True, 'data': "无法认证，尝试其他支付方法"}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'error': True, 'data': "别把你家猫往摄像头上放"}), content_type='application/json')
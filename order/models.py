# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from shop.models import *

# Create your models here.


# 0已生成1已支付2已确认
class Order(models.Model):
    buyer_id = models.IntegerField()
    datetime = models.DateTimeField()
    price = models.IntegerField()
    state = models.IntegerField()


class OrderItem(models.Model):
    item = models.OneToOneField(Item)
    order = models.ForeignKey(Order)

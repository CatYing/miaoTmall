# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from shop.models import *

# Create your models here.


class Order(models.Model):
    buyer_id = models.IntegerField()
    seller_id = models.IntegerField()
    datetime = models.DateTimeField()
    price = models.IntegerField()
    state = models.IntegerField()


class OrderItem(models.Model):
    item = models.OneToOneField(Item)

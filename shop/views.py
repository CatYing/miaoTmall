# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView
from website.mixin import FrontMixin
from django.shortcuts import render
# Create your views here.


class ShopDetailView(FrontMixin, ListView):


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from authentication.models import MyUser

# Create your models here.


class Prototype(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=128)
    prototype = models.ForeignKey(Prototype)
    myuser = models.ForeignKey(MyUser)
    detail = models.TextField()
    available = models.BooleanField(default=True)

    def __unicode__(self):
        return self.myuser.user.username + "的种类为" + self.prototype.name + self.name


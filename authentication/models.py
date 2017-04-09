# coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class RealInfo(models.Model):
    real_name = models.CharField(max_length=64)
    id_number = models.CharField(max_length=32)

    def __unicode__(self):
        return u'某用户的真实信息'


class MyUser(models.Model):
    """
    nickname: 昵称
    real_info:
    """
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=64)
    real_info = models.OneToOneField(RealInfo, blank=True, null=True)
    cellphone = models.CharField(max_length=16)
    address = models.CharField(max_length=512, blank=True)
    head_img = models.ImageField(upload_to='image/%Y/%m/%d', null=True)
    level = models.IntegerField(default=1)
    current_stage = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username

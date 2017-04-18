# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from authentication.models import *

# Create your models here.


class SendingMessage(models.Model):
    datetime = models.DateTimeField()
    content = models.TextField()


class ReceivingMessage(models.Model):
    datetime = models.DateTimeField()
    content = models.TextField()

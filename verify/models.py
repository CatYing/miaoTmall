from __future__ import unicode_literals

from django.db import models

# Create your models here.


class VerifyCode(models.Model):
    available = models.BooleanField()
    code = models.CharField(max_length=16)

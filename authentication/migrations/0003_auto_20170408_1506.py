# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 15:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20170408_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='real_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.RealInfo'),
        ),
    ]
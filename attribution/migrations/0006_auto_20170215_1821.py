# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-15 17:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attribution', '0005_auto_20170203_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationcharge',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='tutorapplication',
            name='uuid',
        ),
    ]

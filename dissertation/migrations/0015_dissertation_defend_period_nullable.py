# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-24 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0014_auto_20161123_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dissertation',
            name='defend_periode',
            field=models.CharField(choices=[('UNDEFINED', 'undefined'), ('JANUARY', 'january'), ('JUNE', 'june'), ('SEPTEMBER', 'september')], default='UNDEFINED', max_length=12, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-04 14:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0021_remove_internshipspeciality_mandatory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internshipspeciality',
            name='order_postion',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-02 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_auto_20180116_1146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='learningcontaineryear',
            old_name='title',
            new_name='common_title',
        ),
        migrations.RenameField(
            model_name='learningcontaineryear',
            old_name='title_english',
            new_name='common_title_english',
        ),
        migrations.RemoveField(
            model_name='learningunityear',
            name='title',
        ),
        migrations.AddField(
            model_name='learningunityear',
            name='specific_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

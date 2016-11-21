# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-21 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0013_remove_propositiondissertation_offer_proposition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dissertationrole',
            name='status',
            field=models.CharField(choices=[('PROMOTEUR', 'promotor'), ('CO_PROMOTEUR', 'copromotor'), ('READER', 'reader'), ('ACCOMPANIST', 'accompanist'), ('INTERNSHIP', 'internship_master'), ('PRESIDENT', 'president')], max_length=12),
        ),
        migrations.AlterField(
            model_name='propositionrole',
            name='status',
            field=models.CharField(choices=[('PROMOTEUR', 'promotor'), ('CO_PROMOTEUR', 'copromotor'), ('READER', 'reader'), ('ACCOMPANIST', 'accompanist'), ('INTERNSHIP', 'internship_master'), ('PRESIDENT', 'president')], default='PROMOTEUR', max_length=12),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-16 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_learningunitcomponent_coefficient_repetition'),
        ('internship', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternshipChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.IntegerField()),
                ('internship_choice', models.IntegerField(default=0)),
                ('priority', models.BooleanField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.Organization')),
                ('speciality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='internship.InternshipSpeciality')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Student')),
            ],
        ),
    ]

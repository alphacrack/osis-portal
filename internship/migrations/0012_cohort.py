# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-27 09:00
from __future__ import unicode_literals

from django.db import migrations, models
import uuid

def createDefaultCohort(apps, schema_editor):
    Cohort = apps.get_model("internship", "Cohort")
    db_alias = schema_editor.connection.alias
    Cohort.objects.using(db_alias).bulk_create([
        Cohort(
            name="M7-2018",
            description="M7-2018",
            free_internships_number=8,
            mandatory_internships_number=0,
            publication_start_date="2017-03-27",
            subscription_start_date="2017-03-01",
            subscription_end_date="2017-03-20")
    ])

def deleteDefaultCohort(apps, schema_editor):
    Cohort = apps.get_model("internship", "Cohort")
    db_alias = schema_editor.connection.alias
    Cohort.objects.filter(pk=1).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0011_periodinternshipplaces'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('free_internships_number', models.IntegerField()),
                ('mandatory_internships_number', models.IntegerField()),
                ('publication_start_date', models.DateField()),
                ('subscription_start_date', models.DateField()),
                ('subscription_end_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(createDefaultCohort, deleteDefaultCohort)
    ]

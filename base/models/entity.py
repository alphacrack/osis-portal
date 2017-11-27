##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Case, When, Q, F
from django.utils import timezone

from base.models.enums import entity_type
from osis_common.models.serializable_model import SerializableModel, SerializableModelAdmin


class EntityAdmin(SerializableModelAdmin):
    list_display = ('id', 'external_id', 'organization', 'location', 'postal_code', 'phone')
    search_fields = ['external_id', 'entityversion__acronym', 'organization__acronym', 'organization__name']
    readonly_fields = ('organization', 'external_id')


class Entity(SerializableModel):
    organization = models.ForeignKey('Organization', blank=True, null=True)
    external_id = models.CharField(max_length=255, unique=True)
    changed = models.DateTimeField(null=True, auto_now=True)

    location = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey('reference.Country', blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "entities"

    def has_address(self):
        return self.location and self.postal_code and self.city

    def __str__(self):
        return "{0} - {1}".format(self.id, self.external_id)

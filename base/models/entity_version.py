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

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils import timezone

from base.models.academic_year import AcademicYear
from base.models.enums import entity_type
from osis_common.models.serializable_model import SerializableModel, SerializableModelAdmin


class EntityVersionAdmin(SerializableModelAdmin):
    list_display = ('id', 'entity', 'acronym', 'parent', 'title', 'entity_type', 'start_date', 'end_date',)
    search_fields = ['entity__id', 'entity__external_id', 'title', 'acronym', 'entity_type', 'start_date', 'end_date']
    raw_id_fields = ('entity', 'parent')
    readonly_fields = ('find_direct_children', 'count_direct_children', 'find_descendants', 'get_parent_version')


class EntityVersionQuerySet(models.QuerySet):
    def current(self, date):
        if date:
            return self.filter(Q(end_date__gte=date) | Q(end_date__isnull=True), start_date__lte=date, )
        else:
            return self

    def entity(self, entity):
        return self.filter(entity=entity)


class EntityVersion(SerializableModel):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed = models.DateTimeField(null=True, auto_now=True)
    entity = models.ForeignKey('Entity')
    title = models.CharField(db_index=True, max_length=255)
    acronym = models.CharField(db_index=True, max_length=20)
    entity_type = models.CharField(choices=entity_type.ENTITY_TYPES, max_length=50, db_index=True, blank=True,
                                   null=True)
    parent = models.ForeignKey('Entity', related_name='parent_of', blank=True, null=True)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True, blank=True, null=True)

    objects = EntityVersionQuerySet.as_manager()

    _descendants = None
    _children = []
    _parent_faculty_version = {}

    def __str__(self):
        return "{} ({} - {} - {} to {})".format(
            self.acronym,
            self.title,
            self.entity_type,
            self.start_date,
            self.end_date
        )

    def save(self, *args, **kwargs):
        if self.can_save_entity_version():
            super(EntityVersion, self).save()
        else:
            raise AttributeError('EntityVersion invalid parameters')

    def can_save_entity_version(self):
        return self.count_entity_versions_same_entity_overlapping_dates() == 0 and \
               self.count_entity_versions_same_acronym_overlapping_dates() == 0 and \
               self.parent != self.entity

    def search_entity_versions_with_overlapping_dates(self):
        if self.end_date:
            qs = EntityVersion.objects.filter(
                Q(start_date__range=(self.start_date, self.end_date)) |
                Q(end_date__range=(self.start_date, self.end_date)) |
                (
                    Q(start_date__lte=self.start_date) & Q(end_date__gte=self.end_date)
                )
            )
        else:
            qs = EntityVersion.objects.filter(
                end_date__gte=self.start_date
            )

        return qs.exclude(id=self.id)

    def count_entity_versions_same_entity_overlapping_dates(self):
        return self.search_entity_versions_with_overlapping_dates().filter(entity=self.entity).count()

    def count_entity_versions_same_acronym_overlapping_dates(self):
        return self.search_entity_versions_with_overlapping_dates().filter(acronym=self.acronym).count()

    def _direct_children(self, date=None):
        if date is None:
            date = timezone.now().date()

        if self._contains_given_date(date):
            return EntityVersion.objects.current(date).filter(parent=self.entity).select_related('entity')

    def find_direct_children(self, date=None):
        if not date:
            direct_children = self.children
        else:
            direct_children = self._direct_children(date)
        return list(direct_children) if direct_children else []

    def count_direct_children(self, date=None):
        return len(self.find_direct_children(date))

    @property
    def descendants(self):
        if not self._descendants:
            self._descendants = self.find_descendants()

        return self._descendants

    @property
    def children(self):
        if not self._children:
            direct_children = self._direct_children()
            self._children = list(direct_children) if direct_children else []
        return self._children

    def find_descendants(self, date=None):
        descendants = []
        direct_children = self.find_direct_children(date)
        if len(direct_children) > 0:
            descendants.extend(direct_children)
            for child in direct_children:
                descendants.extend(child.find_descendants(date))

        return sorted(descendants, key=lambda an_entity: an_entity.acronym)

    def find_parent_faculty_version(self, academic_yr):
        if not isinstance(academic_yr, AcademicYear):
            return None
        if not self._parent_faculty_version.get(academic_yr.id):
            parent_entity = getattr(self, "parent")
            if parent_entity:
                parent_entity_version = find_latest_version_by_entity(parent_entity, academic_yr.start_date)
                if parent_entity_version:
                    if parent_entity_version.entity_type == entity_type.FACULTY:
                        self._parent_faculty_version[academic_yr.id] = parent_entity_version
                    else:
                        self._parent_faculty_version[academic_yr.id] = parent_entity_version.find_parent_faculty_version(academic_yr)
        return self._parent_faculty_version.get(academic_yr.id)

    def get_parent_version(self, date=None):
        if date is None:
            date = timezone.now().date()

        if self._contains_given_date(date):
            qs = EntityVersion.objects.current(date).entity(self.parent)
            try:
                return qs.get()
            except ObjectDoesNotExist:
                return None

    def _contains_given_date(self, date):
        if self.start_date and self.end_date:
            return self.start_date <= date <= self.end_date
        elif self.start_date and not self.end_date:
            return self.start_date <= date
        else:
            return False


def find(acronym, date=None):
    if date is None:
        date = timezone.now()
    try:
        entity_version = EntityVersion.objects.get(acronym=acronym,
                                                   start_date__lte=date,
                                                   end_date__gte=date
                                                   )
    except ObjectDoesNotExist:
        return None

    return entity_version


def find_latest_version(date):
    return EntityVersion.objects.current(date).order_by('-start_date')


def get_last_version(entity, date=None):
    qs = EntityVersion.objects.current(date).entity(entity)

    return qs.latest('start_date')


def search(**kwargs):
    queryset = EntityVersion.objects

    if 'entity' in kwargs:
        queryset = queryset.filter(entity__exact=kwargs['entity'])

    if 'title' in kwargs:
        queryset = queryset.filter(title__exact=kwargs['title'])

    if 'acronym' in kwargs:
        queryset = queryset.filter(acronym__icontains=kwargs['acronym'])

    if 'entity_type' in kwargs:
        queryset = queryset.filter(entity_type__exact=kwargs['entity_type'])

    if 'start_date' in kwargs:
        queryset = queryset.filter(start_date__exact=kwargs['start_date'])

    if 'end_date' in kwargs:
        queryset = queryset.filter(end_date__exact=kwargs['end_date'])

    return queryset.select_related('parent')


def count(**kwargs):
    return search(**kwargs).count()


def find_latest_version_by_entity(entity, date):
    return EntityVersion.objects.current(date).entity(entity).select_related('entity', 'parent').first()

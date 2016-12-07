##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
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

from django.utils.translation import ugettext_lazy as _

CHECKBOX = 'CHECKBOX'
DROPDOWN_LIST = 'DROPDOWN_LIST'
RADIO_BUTTON = 'RADIO_BUTTON'

QUESTION_TYPES = (
    ('LABEL', _('label')),
    ('SHORT_INPUT_TEXT', _('short_input_text')),
    ('LONG_INPUT_TEXT', _('long_input_text')),
    ('RADIO_BUTTON', _('radio_button')),
    ('CHECKBOX', _('checkbox')),
    ('DROPDOWN_LIST', _('dropdown_list')),
    ('UPLOAD_BUTTON', _('Upuload_button')),
    ('DOWNLOAD_LINK', _('download_link')),
    ('HTTP_LINK', _('HTTP_link')))
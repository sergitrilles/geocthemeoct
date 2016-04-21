# -*- coding: utf-8 -*-
import collections
import logging
import datetime
import os
import re
import time
import sys

from pylons import config
from ckan.lib.cli import CkanCommand
from ckan.logic import ValidationError
import ckan.plugins.toolkit as toolkit
import xml.etree.ElementTree as ET
from slugify import slugify

class TranslateEurovoc(CkanCommand):
  """
  """
  summary = __doc__.split('\n')[0]
  usage = __doc__
  max_args = 0
  min_args = 0

  def __init__(self, name):
    super(TranslateEurovoc, self).__init__(name)

  def command(self):
    """
    """
    self._load_config()
    log = logging.getLogger(__name__)

    import ckan.model as model


    log.info('TRANSLATING GROUPS (Eurovoc Domains)')
    root = ET.parse('ckanext/eurovoc/eurovoc_xml/dom_sv.xml').getroot()

    for record in root.iter('RECORD'):
      id = record.find('DOMAINE_ID').text
      context = {'user': 'default', 'model': model, 'session': model.Session}
      group = toolkit.get_action('group_show')(context, {'id': id})
      title = record.find('LIBELLE').text.title()
      log.info('Translating group: ' + id + ' - ' + group['title'] + ' -> ' + title)
      context = {'user': 'default', 'model': model, 'session': model.Session}
      term_dict = {'term': group['title'], 'term_translation': title, 'lang_code': 'sv'}
      toolkit.get_action('term_translation_update')(context, term_dict)

    log.info('TRANSLATING VOCABULARY THESAURUS')

    thesroot = ET.parse('ckanext/eurovoc/eurovoc_xml/thes_sv.xml').getroot()
    thesroot_en = ET.parse('ckanext/eurovoc/eurovoc_xml/thes_en.xml').getroot()

    for record in thesroot_en.iter('RECORD'):
      id = record.find('THESAURUS_ID').text
      title = record.find('LIBELLE').text.title()
      name = re.sub(r'(:S|\'[sS])', r's', title)
      name = re.sub(u'[^a-zA-Z0-9]', r' ', name)
      name = re.sub(u'\s+', r'-', name)
      for sv_record in thesroot.iter('RECORD'):
        id_sv = sv_record.find('THESAURUS_ID').text
        if id_sv == id:
          title_sv = sv_record.find('LIBELLE').text.title()
          name_sv = re.sub(r':S', r's', title_sv)
          name_sv = re.sub(u'[^a-zA-Z0-9åäöÅÄÖ]', r' ', name_sv)
          name_sv = re.sub(u'\s+', r'-', name_sv)
          log.info('Translating tag: ' + id + ' - ' + name + ' -> ' + name_sv)
          context = {'user': 'default', 'model': model, 'session': model.Session}
          term_dict = {'term': name, 'term_translation': name_sv, 'lang_code': 'sv'}
          toolkit.get_action('term_translation_update')(context, term_dict)
          break

# DELETE FROM "group_extra_revision" WHERE group_id = '04';
# DELETE FROM "group_extra" WHERE group_id = '04';
# DELETE FROM "group_role" WHERE group_id = '04';
# DELETE FROM "member_revision" WHERE group_id = '04';
# DELETE FROM "member" WHERE group_id = '04';
# DELETE FROM "group_revision" WHERE id = '04';
# DELETE FROM "group" WHERE id = '04';

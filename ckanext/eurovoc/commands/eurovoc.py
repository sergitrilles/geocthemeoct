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

class InitEurovoc(CkanCommand):
  """
  """
  summary = __doc__.split('\n')[0]
  usage = __doc__
  max_args = 0
  min_args = 0

  def __init__(self, name):
    super(InitEurovoc, self).__init__(name)

  def command(self):
    """
    """
    self._load_config()
    log = logging.getLogger(__name__)

    import ckan.model as model


    log.info('ADDING GROUPS (Eurovoc Domains)')
    root = ET.parse('ckanext/eurovoc/eurovoc_xml/dom_en.xml').getroot()

    for record in root.iter('RECORD'):
      id = record.find('DOMAINE_ID').text
      title = record.find('LIBELLE').text.title()
      name = slugify(title).lower()
      desc = 'Eurovoc Domain: ' + id + ' ' + title
      grp_dict = {'id': id, 'title': title, 'name': name, 'type': 'group', 'extras': [{'key': 'Eurovoc Domain', 'value': title}, {'key': 'Eurovoc Domain ID', 'value': id}]}
      log.info('Creating group: ' + id + ' - ' + title)
      context = {'user': 'default', 'model': model, 'session': model.Session}
      try:
        toolkit.get_action('group_create')(context, grp_dict)
      except:
        pass

    log.info('ADDING VOCABULARY THESAURUS')

    context = {'user': 'default', 'model': model, 'session': model.Session}
    voc_dict = {'name': 'eurovoc_thesaurus'}
    try:
      voc = toolkit.get_action('vocabulary_create')(context, voc_dict)
    except ValidationError, e:
      voc = toolkit.get_action('vocabulary_show')(context, {'id': 'eurovoc_thesaurus'})

    thesroot = ET.parse('ckanext/eurovoc/eurovoc_xml/thes_en.xml').getroot()

    for record in thesroot.iter('RECORD'):
      id = record.find('THESAURUS_ID').text
      title = record.find('LIBELLE').text.title()
      name = slugify(title)
      name_new = re.sub(r'(:S|\'[sS])', r's', title)
      name_new = re.sub(u'[^a-zA-Z0-9]', r' ', name_new)
      name_new = re.sub(u'\s+', r'-', name_new)
      log.info('Creating tag: ' + name_new)
      context = {'user': 'default', 'model': model, 'session': model.Session}
      del_dict = {'id': name, 'vocabulary_id': voc['id']}
      try:
        toolkit.get_action('tag_delete')(context, del_dict)
      except:
        pass
      del_dict['id'] = name_new
      try:
        toolkit.get_action('tag_delete')(context, del_dict)
      except:
        pass
      tag_dict = {'name': name_new, 'vocabulary_id': voc['id']}
      context = {'user': 'default', 'model': model, 'session': model.Session}
      toolkit.get_action('tag_create')(context, tag_dict)

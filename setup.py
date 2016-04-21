from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(
	name='ckanext-opendata',
	version=version,
	description="Extension for oppnadata",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Michael J\xc3\xb6nsson/Johan Walther/Joakim Bengtson',
	author_email='michael.jonsson@softhouse.se',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.eurovoc', 'ckanext.blog', 'ckanext.opendata'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
        "python-slugify >= 0.0.6"
	],
    	message_extractors = {
        'ckan': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('templates/importer/**', 'ignore', None),
            ('templates/**.html', 'ckan', None),
            ('templates_legacy/**.html', 'ckan', None),
            ('ckan/templates/home/language.js', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
            ('templates/**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
            ('templates_legacy/**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
            ('public/**', 'ignore', None),
        ],
        'ckanext-opendata': [
            ('**.py', 'python', None),
            ('**.html', 'ckan', None),
            ('multilingual/solr/*.txt', 'ignore', None),
            ('**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
        ],
        'ckanext-eurovoc': [
            ('**.py', 'python', None),
            ('**.html', 'ckan', None),
            ('multilingual/solr/*.txt', 'ignore', None),
            ('**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
        ],
        'ckanext-blog': [
            ('**.py', 'python', None),
            ('**.html', 'ckan', None),
            ('multilingual/solr/*.txt', 'ignore', None),
            ('**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
        ],
        'ckanext': [
            ('**.py', 'python', None),
            ('**.html', 'ckan', None),
            ('multilingual/solr/*.txt', 'ignore', None),
            ('**.txt', 'genshi', {
                'template_class': 'genshi.template:TextTemplate'
            }),
        ]
	},
	entry_points=\
  """
      [ckan.plugins]
      eurovoc = ckanext.eurovoc.plugin:EurovocDatasetFormPlugin
      blog = ckanext.blog.plugin:BlogPlugin
      opendata = ckanext.opendata.plugin:OpenDataPlugin

      [paste.paster_command]
      inventory_init = ckanext.blog.commands.inventory_init:InitDB
      eurovoc_init = ckanext.eurovoc.commands.eurovoc:InitEurovoc
      eurovoc_trans = ckanext.eurovoc.commands.eurovoc_trans:TranslateEurovoc
  """,
)

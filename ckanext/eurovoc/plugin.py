import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk


def eurovoc_thesauruses():
    '''Return the list of eurovoc thesaurus tags from the eurovoc thesaurus vocabulary.'''
    try:
        eurovoc_thesaurus = tk.get_action('tag_list')(
                data_dict={'vocabulary_id': 'eurovoc_thesaurus'})
        return eurovoc_thesaurus
    except tk.ObjectNotFound:
        return None

def eurovoc_domains():
    '''Return the list of eurovoc domain groups from the eurovoc domain vocabulary.'''
    try:
        eurovoc_domains = tk.get_action('group_list')(
                data_dict={'all_fields': True})
        return eurovoc_domains
    except tk.ObjectNotFound:
        return None


class EurovocDatasetFormPlugin(plugins.SingletonPlugin,
        tk.DefaultDatasetForm):
    '''An Eurovoc IDatasetForm CKAN plugin.

    Uses a tag vocabulary to add a custom metadata field to datasets.

    '''
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IDatasetForm, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)
    plugins.implements(plugins.IFacets, inherit=True)

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')

        config['search.facets'] = 'groups vocab_eurovoc_thesaurus tags res_format license_id'

    def get_helpers(self):
        return {'eurovoc_thesauruses': eurovoc_thesauruses, 'eurovoc_domains': eurovoc_domains}

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        # Add our custom eurovoc_thesaurus metadata field to the schema.
        schema.update({
                'eurovoc_thesaurus': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_tags')('eurovoc_thesaurus')]
                })
        # Add our custom_test metadata field to the schema, this one will use
        # convert_to_extras instead of convert_to_tags.
        # schema.update({
        #         'custom_text': [tk.get_validator('ignore_missing'),
        #             tk.get_converter('convert_to_extras')]
        #         })
        return schema

    def create_package_schema(self):
        schema = super(EurovocDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(EurovocDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(EurovocDatasetFormPlugin, self).show_package_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        # Add our custom eurovoc_thesaurus metadata field to the schema.
        schema.update({
            'eurovoc_thesaurus': [
                tk.get_converter('convert_from_tags')('eurovoc_thesaurus'),
                tk.get_validator('ignore_missing')]
            })

        # Add our custom_text field to the dataset schema.
        # schema.update({
        #     'custom_text': [tk.get_converter('convert_from_extras'),
        #         tk.get_validator('ignore_missing')]
        #     })

        return schema

    # These methods just record how many times they're called, for testing
    # purposes.
    # TODO: It might be better to test that custom templates returned by
    # these methods are actually used, not just that the methods get
    # called.

    def setup_template_variables(self, context, data_dict):
        return super(EurovocDatasetFormPlugin, self).setup_template_variables(
                context, data_dict)

    def new_template(self):
        return super(EurovocDatasetFormPlugin, self).new_template()

    def read_template(self):
        return super(EurovocDatasetFormPlugin, self).read_template()

    def edit_template(self):
        return super(EurovocDatasetFormPlugin, self).edit_template()

    def search_template(self):
        return super(EurovocDatasetFormPlugin, self).search_template()

    def history_template(self):
        return super(EurovocDatasetFormPlugin, self).history_template()

    def package_form(self):
        return super(EurovocDatasetFormPlugin, self).package_form()

    def dataset_facets(self, facets_dict, package_type):
        facets_dict.update({
            'vocab_eurovoc_thesaurus' : tk._('Eurovoc') + ' ' + tk._('Sub group')
        })
        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        return facets_dict

from logging import getLogger

import ckan.plugins as p
import ckan.lib.base as base
import ckan.lib.helpers as helpers
import ckanext.multilingual.plugin as multil

log = getLogger(__name__)

proxy = False
try:
    import ckanext.resourceproxy.plugin as proxy
except ImportError:
    pass



class OpenDataPlugin(p.SingletonPlugin):
    """This extension previews PDFs

    This extension implements two interfaces

      - ``IConfigurer`` allows to modify the configuration
      - ``IConfigurable`` get the configuration
      - ``IResourcePreview`` allows to add previews
    """
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IResourcePreview, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    proxy_is_enabled = False

    def get_helpers(self):
        """
        A dictionary of extra helpers that will be available to provide
        dgu specific helpers to the templates.  We may be able to override
        h.linked_user so that we don't need to monkey patch above.
        """
        from inspect import getmembers, isfunction

        helper_dict = {}

        functions_list = [o for o in getmembers(helpers, isfunction)]
        for name, fn in functions_list:
            if name[0] != '_':
                helper_dict[name] = fn

        helper_dict['trans_dict'] = multil.translate_data_dict

        return helper_dict


    def update_config(self, config):
        ''' Set up the resource library, public directory and
        template directory for the preview
        '''
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_template_directory(config, 'theme/templates')
        p.toolkit.add_resource('theme/public', 'ckanext-opendata')

    def configure(self, config):
        self.proxy_is_enabled = config.get('ckan.resource_proxy_enabled', False)

    # def can_preview(self, data_dict):
    #     resource = data_dict['resource']
    #     format_lower = resource['format'].lower()
    #     return format_lower in self.PDF and (resource['on_same_domain'] or self.proxy_is_enabled)

    def setup_template_variables(self, context, data_dict):
        if self.proxy_is_enabled and not data_dict['resource']['on_same_domain']:
            base.c.resource['url'] = proxy.get_proxified_resource_url(data_dict)

# -*- coding: utf-8 -*-

from zope.component import queryUtility, getMultiAdapter

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.analytics.view import AnalyticsViewlet as BaseAnalyticsViewlet

from collective.analyticspanel.interfaces import IAnalyticsSettings

class AnalyticsViewlet(BaseAnalyticsViewlet):
    
    def cleanup_path(self, path):
        """Given a path, cleanup trailing slashes and add to it portal id"""
        plone_tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        portal_id = plone_tools.url().getPortalObject().getId()

        if not path.startswith('/'):
            path = "/%s" % path

        if not path.startswith('/%s' % portal_id):
            path = "/%s%s" % (portal_id, path)
        
        if path.endswith('/'):
            path = path[:-1]
        
        return path
    
    def render(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IAnalyticsSettings, check=False)
        
        error_type = self.request.get('error_type', None)
        context_path = '/'.join(self.context.getPhysicalPath())

        # 1 - error code take precedence
        if error_type and settings.error_specific_code:
            for possible_error in settings.error_specific_code:
                message = possible_error.message 
                if message==error_type:
                    return safe_unicode(possible_error.message_snippet)

        # 2 - path specific snippet
        if settings.path_specific_code:
            best_path = best_code = ''
            for possible_path in settings.path_specific_code:
                path = self.cleanup_path(possible_path.path)
                # Apply to while subtree?
                if getattr(possible_path, 'apply_to_subsection', True):
                    if context_path.startswith(path) and len(path)>len(best_path):
                        best_path = path
                        best_code = possible_path.path_snippet
                # do not apply to the subsection
                elif context_path==path:
                    return safe_unicode(possible_path.path_snippet)
            if best_path:
                return safe_unicode(best_code)

        return safe_unicode(settings.general_code)

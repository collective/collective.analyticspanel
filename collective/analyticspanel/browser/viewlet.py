# -*- coding: utf-8 -*-

from zope.component import queryUtility, getMultiAdapter

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.analytics.view import AnalyticsViewlet as BaseAnalyticsViewlet

from collective.analyticspanel.interfaces import IAnalyticsSettingsSchema

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
        settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)
        
        error_type = self.request.get('error_type', None)

        context = self.context
        context_physical_path = context.getPhysicalPath()
        context_path = '/'.join(context_physical_path)
        parent_path = '/'.join(context_physical_path[:-1])

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
                # Apply to whole subtree?
                if getattr(possible_path, 'apply_to', '') == u'subtree':
                    if context_path.startswith(path) and len(path)>len(best_path):
                        best_path = path
                        best_code = possible_path.path_snippet
                # Apply to the context only (do not apply to the subsection or children)
                elif getattr(possible_path, 'apply_to', '') in (u'context', u'context_and_children') and context_path==path:
                    return safe_unicode(possible_path.path_snippet)
                # Apply to the context if is not folderish and a proper configuration exits for the parent
                elif getattr(possible_path, 'apply_to', '') == u'context_and_children' and parent_path==path:
                    if not context.portal_type in settings.folderish_types:
                        return safe_unicode(possible_path.path_snippet)
            if best_path:
                return safe_unicode(best_code)
        return safe_unicode(settings.general_code)

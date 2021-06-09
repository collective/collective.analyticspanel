# -*- coding: utf-8 -*-

from zope.component import queryUtility, getMultiAdapter
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.analytics.view import AnalyticsViewlet as BaseAnalyticsViewlet
from collective.analyticspanel.interfaces import IAnalyticsSettingsSchema


class AnalyticsViewlet(BaseAnalyticsViewlet):
    """Base class for Analytics. As Plone default it will put analytics in the footer"""

    position = 'footer'

    def cleanup_path(self, path):
        """Given a path, cleanup trailing slashes and add to it portal's path"""
        plone_tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        portal_path = plone_tools.url().getPortalPath()

        if not path.startswith('/'):
            path = "/%s" % path

        if not path.startswith(portal_path):
            path = portal_path + path

        if path.endswith('/'):
            path = path[:-1]

        return path

    def render(self):
        # Don't show analytics views called in overlays (so with ajax_load paramiter)
        if self.request.get_header('X-Requested-With')=='XMLHttpRequest' or self.request.form.get('ajax_load'):
            return ""
        # A lot of getattr here to prevent errors when upgrading to 0.4 version
        # before running upgrade step
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)

        # *** Privacy ***
        if getattr(settings, 'respect_donottrack', None) and self.request.get_header('HTTP_DNT') == '1':
            return ''
        if getattr(settings, 'respect_optout', None) and self.request.cookies.get('analytics-optout', None) == 'true':
            return ''
        if getattr(settings, 'force_optin', None) and self.request.cookies.get('analytics-optout', None) != 'false':
            return ''
        
        # ---- cookiebot addon ------
        exclude_subdomains = ["dev", "design", "staging"]
        if any(subdomain in self.request.base for subdomain in exclude_subdomains):
            return '<!-- exclude cookiebot from dev/design/staging -->'

        error_type = self.request.get('error_type', None)

        context = self.context
        context_physical_path = context.getPhysicalPath()
        context_path = '/'.join(context_physical_path)
        parent_path = '/'.join(context_physical_path[:-1])

        # 1 - error code take precedence
        if error_type and settings.error_specific_code:
            for possible_error in settings.error_specific_code:
                message = possible_error.message
                position = getattr(possible_error, 'position', 'footer')
                if message==error_type and position==self.position:
                    return safe_unicode(possible_error.message_snippet)

        # 2 - path specific snippet
        if settings.path_specific_code:
            best_path = best_code = ''
            for possible_path in settings.path_specific_code:
                position = getattr(possible_path, 'position', 'footer')
                if position!=self.position:
                    continue
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
        if self.position=='footer':
            return safe_unicode(settings.general_code)
        return safe_unicode(getattr(settings, 'general_header_code', ''))


class HeaderAnalyticsViewlet(AnalyticsViewlet):

    position = 'header'

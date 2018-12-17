# -*- coding: utf-8 -*-

from zope.component import queryUtility, getMultiAdapter
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.analytics.view import (
    AnalyticsViewlet as BaseAnalyticsViewlet,
)
from collective.analyticspanel.interfaces import IAnalyticsSettingsSchema


class AnalyticsViewlet(BaseAnalyticsViewlet):
    """
    Base class for Analytics.
    As Plone default it will put analytics in the footer
    """

    position = 'footer'

    def cleanup_path(self, path):
        """
        Given a path, cleanup trailing slashes and add to it portal's path
        """
        plone_tools = getMultiAdapter(
            (self.context, self.request), name=u'plone_tools'
        )
        portal_path = plone_tools.url().getPortalPath()

        if not path.startswith('/'):
            path = "/%s" % path

        if not path.startswith(portal_path):
            path = portal_path + path

        if path.endswith('/'):
            path = path[:-1]

        return path

    def render(self):
        # Don't show analytics views called in overlays (so with ajax_load parameter)  # noqa
        if self.request.get_header(
            'X-Requested-With'
        ) == 'XMLHttpRequest' or self.request.form.get('ajax_load'):
            return ""
        # A lot of getattr here to prevent errors when upgrading to 0.4 version
        # before running upgrade step
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)
        # *** Privacy ***
        # If analytics-optout is false we should ignore also the DNT header.
        # If not...
        if (
            getattr(settings, 'respect_optout', None)
            and self.request.cookies.get('analytics-optout', None) != 'false'
        ):
            if (
                getattr(settings, 'respect_donottrack', None)
                and self.request.get_header('HTTP_DNT') == '1'
            ):
                return ''
            if (
                getattr(settings, 'respect_optout', None)
                and self.request.cookies.get('analytics-optout', None) == 'true'
            ):
                return ''

        error_type = self.request.get('error_type', None)

        context = self.context
        context_physical_path = context.getPhysicalPath()
        context_path = '/'.join(context_physical_path)
        parent_path = '/'.join(context_physical_path[:-1])

        # 1 - error code take precedence
        if error_type and settings.error_specific_code:
            for possible_error in settings.error_specific_code:
                message = possible_error.get('message', '')
                position = possible_error.get('position', 'footer')
                if message == error_type and position == self.position:
                    return safe_unicode(possible_error.get('message_snippet'))

        # 2 - path specific snippet
        if settings.path_specific_code:
            best_path = best_code = ''
            for possible_path in settings.path_specific_code:
                position = possible_path.get('position', 'footer')
                if position != self.position:
                    continue
                path = self.cleanup_path(possible_path.get('path', ''))
                # Apply to whole subtree?
                if possible_path.get('apply_to', '') == u'subtree':
                    if context_path.startswith(path) and len(path) > len(
                        best_path
                    ):
                        best_path = path
                        best_code = possible_path.get('path_snippet', '')
                # Apply to the context only
                # (do not apply to the subsection or children)
                elif (
                    possible_path.get('apply_to', '')
                    in (u'context', u'context_and_children')
                    and context_path == path
                ):
                    return safe_unicode(possible_path.get('path_snippet', ''))
                # Apply to the context if is not folderish and a proper
                # configuration exits for the parent
                elif (
                    possible_path.get('apply_to', '') == u'context_and_children'
                    and parent_path == path
                ):
                    if context.portal_type not in settings.folderish_types:
                        return safe_unicode(
                            possible_path.get('path_snippet', '')
                        )
            if best_path:
                return safe_unicode(best_code)
        if self.position == 'footer':
            return safe_unicode(settings.general_code)
        return safe_unicode(getattr(settings, 'general_header_code', ''))


class HeaderAnalyticsViewlet(AnalyticsViewlet):

    position = 'header'

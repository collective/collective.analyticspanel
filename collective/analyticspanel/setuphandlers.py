# -*- coding: utf-8 -*-

from zope.component import queryUtility

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode

from collective.analyticspanel import logger

from collective.analyticspanel.interfaces import IAnalyticsSettings

def setupVarious(context):
    if context.readDataFile('collective.analyticspanel_various.txt') is None:
        return

    portal = context.getSite()
    
    ptool = portal.portal_properties
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IAnalyticsSettings, check=False)

    if settings.general_code:
        logger.info('Already found a local analytics code in my registry: no operation taken')
        return

    plone_snippet = ptool.site_properties.webstats_js
    
    if plone_snippet:
        logger.info('Found a general analytics code: copying it in my registry')
        settings.general_code = safe_unicode(ptool.site_properties.webstats_js)


def migrateTo1001(context):
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IAnalyticsSettings, check=False)
    for path_config in settings.path_specific_code:
        if not hasattr(path_config, 'apply_to_subsection'):
            path_config.apply_to_subsection = True
            logger.info('Added new boolean property "apply_to_subsection" to %s' % safe_unicode(path_config.path))
    logger.info('Migrated to version 0.2')

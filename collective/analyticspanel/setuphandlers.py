# -*- coding: utf-8 -*-

from zope.component import queryUtility

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode

from collective.analyticspanel.interfaces import IAnalyticsSettings

def setupVarious(context):
    if context.readDataFile('collective.analyticspanel_various.txt') is None:
        return

    logger = context.getLogger('collective.analyticspanel')
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

    
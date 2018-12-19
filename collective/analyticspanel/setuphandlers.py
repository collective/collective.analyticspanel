# -*- coding: utf-8 -*-
from collective.analyticspanel import logger
from collective.analyticspanel.interfaces import IAnalyticsSettings
from collective.analyticspanel.interfaces import IAnalyticsSettingsSchema
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from zope.component import queryUtility

try:
    from Products.CMFPlone.interfaces.controlpanel import ISiteSchema

    PLONE_4 = False
except ImportError:
    PLONE_4 = True

PROFILE_ID = 'profile-collective.analyticspanel:default'


def setupVarious(context):
    if context.readDataFile('collective.analyticspanel_various.txt') is None:
        return

    portal = context.getSite()

    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)

    if settings.general_code:
        logger.info(
            'Already found a local analytics code in my registry: no operation taken'
        )
        return

    old_js_config = getOldJsConfig(portal, registry)

    if old_js_config:
        logger.info('Found a general analytics code: copying it in my registry')
        settings.general_code = safe_unicode(old_js_config)


def getOldJsConfig(portal, registry):
    if PLONE_4:
        ptool = portal.portal_properties
        return getattr(ptool.site_properties, 'webstats_js', None)
    else:
        site = registry.forInterface(ISiteSchema, prefix="plone")
        return site.webstats_js


def migrateTo1001(context):
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IAnalyticsSettings, check=False)
    for path_config in settings.path_specific_code:
        if not hasattr(path_config, 'apply_to_subsection'):
            path_config.apply_to_subsection = True
            logger.info(
                'Added new boolean property "apply_to_subsection" to %s'
                % safe_unicode(path_config.path)
            )
    logger.info('Migrated to version 0.2')


def migrateTo1020(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')

    registry = queryUtility(IRegistry)
    old_settings = registry.forInterface(IAnalyticsSettings, check=False)
    new_settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)
    if old_settings.general_code and not new_settings.general_code:
        new_settings.general_code = old_settings.general_code
        logger.info('Migrating general_code')
    if not new_settings.error_specific_code:
        for error_config in old_settings.error_specific_code:
            new_settings.error_specific_code += (error_config,)
            logger.info(
                'Migrating an error_specific_code record for code %s'
                % error_config.message
            )
    if not new_settings.path_specific_code:
        for path_config in old_settings.path_specific_code:
            apply_to_subsection = path_config.apply_to_subsection
            del path_config.apply_to_subsection
            if apply_to_subsection:
                path_config.apply_to = u'subtree'
            else:
                path_config.apply_to = u'context'
            new_settings.path_specific_code += (path_config,)
            logger.info(
                'Migrating a path_specific_code record for path %s'
                % path_config.path
            )
    setup_tool.runAllImportStepsFromProfile(
        'profile-collective.analyticspanel:registry_cleanup'
    )
    logger.info('Registry cleanup operation performed')
    logger.info('Migrated to version 0.3')


def migrateTo1100(context):
    setup_tool = getToolByName(context, 'portal_setup')
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)
    # 1. Nullify fields
    logger.info('Cleaning old registrations')
    settings.error_specific_code = []
    settings.path_specific_code = []
    # 2. registering new data
    logger.info('Import new migrated data')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    logger.info('Migrated to version 0.4')


def migrateTo1200(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    logger.info('Migrated to version 0.5')


def migrateTo2000(context):
    """
    Replace Persistent Objects with standard list of dictionaries
    and collective.z3cform.datagridfield
    """

    def convert_persistent_data(data):
        return data.__Broken_state__

    setup_tool = api.portal.get_tool(name='portal_setup')
    setup_tool.runAllImportStepsFromProfile(
        'profile-collective.z3cform.datagridfield:default'
    )
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)
    error_specific_code_value = map(
        convert_persistent_data, settings.error_specific_code
    )
    path_specific_code_value = map(
        convert_persistent_data, settings.path_specific_code
    )
    # delete old records
    del registry.records[
        'collective.analyticspanel.interfaces.IAnalyticsSettingsSchema.error_specific_code'  # noqa
    ]
    del registry.records[
        'collective.analyticspanel.interfaces.IAnalyticsSettingsSchema.path_specific_code'  # noqa
    ]
    # re-import
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')

    # save new values
    settings.error_specific_code = error_specific_code_value
    settings.path_specific_code = path_specific_code_value

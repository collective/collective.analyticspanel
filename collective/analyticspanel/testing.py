# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from plone import api

try:
    from Products.CMFPlone.interfaces.controlpanel import ISiteSchema

    PLONE_4 = False
except ImportError:
    PLONE_4 = True

import collective.analyticspanel
import collective.z3cform.datagridfield


class AnalyticsPanelLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.z3cform.datagridfield)
        self.loadZCML(package=collective.analyticspanel)

    def setUpPloneSite(self, portal):
        if PLONE_4:
            portal.portal_properties.site_properties.webstats_js = (
                'SITE DEFAULT ANALYTICS'
            )
        else:
            registry = queryUtility(IRegistry)
            site = registry.forInterface(ISiteSchema, prefix="plone")
            site.webstats_js = u'SITE DEFAULT ANALYTICS'

        applyProfile(portal, 'collective.analyticspanel:default')


ANALYTICS_PANEL_FIXTURE = AnalyticsPanelLayer()


ANALYTICS_PANEL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ANALYTICS_PANEL_FIXTURE,),
    name='AnalyticsPanelLayer:IntegrationTesting',
)


ANALYTICS_PANEL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ANALYTICS_PANEL_FIXTURE,),
    name='AnalyticsPanelLayer:FunctionalTesting',
)

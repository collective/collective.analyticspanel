# -*- coding: utf-8 -*-

from zope.configuration import xmlconfig

from plone.testing import z2

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

class AnalyticsPanel(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.analyticspanel
        xmlconfig.file('configure.zcml',
                       collective.analyticspanel,
                       context=configurationContext)
        z2.installProduct(app, 'collective.analyticspanel')

    def setUpPloneSite(self, portal):
        portal.portal_properties.site_properties.webstats_js = 'SITE DEFAULT ANALYTICS'
        applyProfile(portal, 'collective.analyticspanel:default')
        #quickInstallProduct(portal, 'collective.analyticspanel')
        setRoles(portal, TEST_USER_ID, ['Member', 'Manager'])


ANALYTICS_PANEL_FIXTURE = AnalyticsPanel()
ANALYTICS_PANEL_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(ANALYTICS_PANEL_FIXTURE, ),
                       name="AnalyticsPanel:Integration")
ANALYTICS_PANEL_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(ANALYTICS_PANEL_FIXTURE, ),
                       name="AnalyticsPanel:Functional")


# -*- coding: utf-8 -*-

from zope.component import queryUtility, getMultiAdapter

from plone.registry.interfaces import IRegistry

from collective.analyticspanel.interfaces import IAnalyticsSettingsSchema
from collective.analyticspanel.testing import ANALYTICS_PANEL_INTEGRATION_TESTING

from .base import BaseTestCase


class TestConfiguration(BaseTestCase):

    layer = ANALYTICS_PANEL_INTEGRATION_TESTING

    def test_default_configuration(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)
        self.assertEqual(settings.general_code, 'SITE DEFAULT ANALYTICS')

    def test_hidden_plone_base_analytics(self):
        portal = self.layer['portal']
        request = self.layer['request']
        self.markRequestWithLayer()
        controlpanel_view = getMultiAdapter((portal, request), name=u'site-controlpanel')
        self.assertTrue('form.webstats_js' not in controlpanel_view())

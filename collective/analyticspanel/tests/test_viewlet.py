# -*- coding: utf-8 -*-

import unittest

from zope.component import queryUtility, getMultiAdapter

from plone.app.testing import applyProfile
from plone.registry.interfaces import IRegistry

from collective.analyticspanel.interfaces import IAnalyticsSettings
from collective.analyticspanel.testing import ANALYTICS_PANEL_INTEGRATION_TESTING
from collective.analyticspanel.pair_fields import ErrorCodeValuePair

from base import BaseTestCase

class TestViewlet(BaseTestCase):

    layer = ANALYTICS_PANEL_INTEGRATION_TESTING

    def test_viewlet_registered(self):
        portal = self.layer['portal']
        self.markRequestWithLayer()
        self.getSettings().general_code = u'SITE ANALYTICS'
        self.assertTrue('SITE ANALYTICS' in portal())

# Do not run this test until p.a.testing will not fix https://dev.plone.org/ticket/11673
#    def test_back_base_viewlet(self):
#        portal = self.layer['portal']
#        applyProfile(portal, 'collective.analyticspanel:uninstall')
#        self.assertTrue('SITE DEFAULT ANALYTICS' in portal())

    def test_not_found(self):
        portal = self.layer['portal']
        request = self.layer['request']
        settings = self.getSettings()

        record = ErrorCodeValuePair()
        record.message = 'NotFound'
        record.message_snippet = u'You are in a NotFound page'

        settings.error_specific_code += (record,)
        request.set('error_type', 'NotFound')
        view = getMultiAdapter((portal, request), name=u"contact-info")
        self.assertTrue('You are in a NotFound page' in view())


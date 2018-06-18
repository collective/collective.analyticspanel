# -*- coding: utf-8 -*-

import socket
import urllib
import urllib2
from urllib2 import HTTPError
import json

from Products.Five import BrowserView

from zope.component import queryUtility, getMultiAdapter
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.analytics.view import AnalyticsViewlet as BaseAnalyticsViewlet
from collective.analyticspanel.interfaces import IAnalyticsSettingsSchema


class AnalyticspanelJsonView(BrowserView):
    
    def render_json(self):
        """
        :return: header and footer analytics code as JSON object
        """
        try:
            registry = queryUtility(IRegistry)
            settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)

            output = ({"header": safe_unicode(getattr(settings, 'general_header_code', '')), "footer": safe_unicode(settings.general_code)})

            return json.dumps(output)

        except:
            return json.dumps(({}))

    def render_plain(self, position):
        """
        :return: header or footer analytics code as plain object
        """
        try:
            registry = queryUtility(IRegistry)
            settings = registry.forInterface(IAnalyticsSettingsSchema, check=False)

            if position == "header":
                output = safe_unicode(getattr(settings, 'general_header_code', ''))
            elif position == "footer":
                output = safe_unicode(settings.general_code)

            return output

        except:
            return ""


    def __call__(self):

        try:
            """
            Start rendering Plain Text
            :return: plain text code
            """
            # setup: header
            self.request.response.setHeader('Content-Type', 'text/plain; charset=utf-8')

            return self.render_plain(self.request.form["position"])

        except KeyError:
            """
            Start rendering JSON
            :return: the JSON result
            """
            # setup: header
            self.request.response.setHeader('Content-Type', 'application/json; charset=utf-8')

            return self.render_json()

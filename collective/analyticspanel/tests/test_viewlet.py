# -*- coding: utf-8 -*-
from .base import BaseTestCase

from collective.analyticspanel.browser.viewlet import AnalyticsViewlet
from collective.analyticspanel.testing import (
    ANALYTICS_PANEL_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter


class TestViewlet(BaseTestCase):

    layer = ANALYTICS_PANEL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_viewlet_registered(self):
        self.markRequestWithLayer()
        self.request.set('ACTUAL_URL', 'http://nohost/plone')
        self.getSettings().general_code = u'SITE ANALYTICS FOOTER'
        self.getSettings().general_header_code = u'SITE ANALYTICS HEADER'
        self.assertTrue('SITE ANALYTICS FOOTER' in self.portal())
        self.assertTrue('SITE ANALYTICS HEADER' in self.portal())

    # Do not run this test until p.a.testing will not fix https://dev.plone.org/ticket/11673
    #    def test_back_base_viewlet(self):
    #        applyProfile(portal, 'collective.analyticspanel:uninstall')
    #        self.assertTrue('SITE DEFAULT ANALYTICS' in portal())

    def test_not_found(self):
        self.request.set('ACTUAL_URL', 'http://nohost/plone')
        self.markRequestWithLayer()
        settings = self.getSettings()

        records = [
            {
                'message': 'NotFound',
                'message_snippet': u'You are in a NotFound page (footer)',
                'position': u'footer',
            },
            {
                'message': 'NotFound',
                'message_snippet': u'You are in a NotFound page (header)',
                'position': 'header',
            },
        ]
        settings.error_specific_code = records

        self.request.set('error_type', 'NotFound')
        view = getMultiAdapter((self.portal, self.request), name=u"sharing")
        self.assertTrue('You are in a NotFound page (footer)' in view())
        self.assertTrue('You are in a NotFound page (header)' in view())

    def test_for_path(self):
        self.portal.invokeFactory(type_name='Folder', id='news', title="News")
        self.request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.markRequestWithLayer()
        settings = self.getSettings()

        records = [
            {
                'path': u'/news',
                'path_snippet': u'You are in the News section (footer)',
                'apply_to': u'subtree',
                'position': u'footer',
            },
            {
                'path': u'/news',
                'path_snippet': u'You are in the News section (header)',
                'apply_to': u'subtree',
                'position': u'header',
            },
        ]
        settings.path_specific_code = records

        self.assertTrue(
            'You are in the News section (footer)' in self.portal.news()
        )
        self.assertTrue(
            'You are in the News section (header)' in self.portal.news()
        )
        self.request.set('ACTUAL_URL', 'http://nohost/plone')
        self.assertFalse('You are in the News section' in self.portal())

    def test_most_specific_path_used(self):
        self.portal.invokeFactory(type_name='Folder', id='news', title="News")
        self.portal.news.invokeFactory(
            type_name='Folder', id='subnews', title="Subfolder inside news"
        )

        self.request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.markRequestWithLayer()
        settings = self.getSettings()

        records = [
            {
                'path': u'/news',
                'path_snippet': u'You are in the News section (footer)',
                'apply_to': u'subtree',
                'position': u'footer',
            },
            {
                'path': u'/news/subnews',
                'path_snippet': u'You are in the Subnews section (footer)',
                'apply_to': u'subtree',
                'position': u'footer',
            },
            {
                'path': u'/news',
                'path_snippet': u'You are in the News section (header)',
                'apply_to': u'subtree',
                'position': u'header',
            },
        ]

        settings.path_specific_code = records

        self.request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.assertTrue(
            'You are in the Subnews section (footer)'
            in self.portal.news.subnews()
        )
        self.assertTrue(
            'You are in the News section (header)' in self.portal.news.subnews()
        )

    def test_hiding_code(self):
        self.portal.invokeFactory(type_name='Folder', id='news', title="News")

        self.request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.markRequestWithLayer()
        settings = self.getSettings()
        settings.general_header_code = u'DEFAULT ANALYTICS IN HEADER'

        self.assertTrue('SITE DEFAULT ANALYTICS' in self.portal.news())
        self.assertTrue('DEFAULT ANALYTICS IN HEADER' in self.portal.news())

        records = [
            {
                'path': u'/news',
                'path_snippet': u'',
                'apply_to': u'subtree',
                'position': 'footer',
            },
            {
                'path': u'/news',
                'path_snippet': u'',
                'apply_to': u'subtree',
                'position': 'header',
            },
        ]

        settings.path_specific_code = records

        self.assertFalse('SITE DEFAULT ANALYTICS' in self.portal.news())
        self.assertFalse('DEFAULT ANALYTICS IN HEADER' in self.portal.news())

    def test_no_subtree_propagation(self):
        self.portal.invokeFactory(type_name='Folder', id='news', title="News")

        self.request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.markRequestWithLayer()
        settings = self.getSettings()
        settings.general_header_code = u'DEFAULT ANALYTICS IN HEADER'

        self.assertTrue('SITE DEFAULT ANALYTICS' in self.portal.news())
        self.assertTrue('DEFAULT ANALYTICS IN HEADER' in self.portal.news())

        records = [
            {
                'path': u'/news',
                'path_snippet': u'Only for news (footer)',
                'apply_to': u'context',
                'position': u'footer',
            },
            {
                'path': u'/news',
                'path_snippet': u'Only for news (header)',
                'apply_to': u'context',
                'position': u'header',
            },
        ]

        settings.path_specific_code = records

        self.assertTrue('Only for news (footer)' in self.portal.news())
        self.assertTrue('Only for news (header)' in self.portal.news())

        self.portal.news.invokeFactory(
            type_name='Folder', id='subnews', title="Subnews"
        )
        self.request.set('ACTUAL_URL', 'http://nohost/plone/news/subnews')

        self.assertTrue('SITE DEFAULT ANALYTICS' in self.portal.news.subnews())
        self.assertTrue(
            'DEFAULT ANALYTICS IN HEADER' in self.portal.news.subnews()
        )

    def test_apply_to_folder_and_children(self):
        self.markRequestWithLayer()
        settings = self.getSettings()
        settings.general_header_code = u'DEFAULT ANALYTICS IN HEADER'
        self.portal.invokeFactory(type_name='Folder', id='news', title="News")
        news = self.portal.news
        news.invokeFactory(type_name='Folder', id='subnews', title="Sub news")
        news.invokeFactory(
            type_name='Document', id='home', title="Homepage for news section"
        )

        records = [
            {
                'path': u'/news',
                'path_snippet': u'For news and children (footer)',
                'apply_to': u'context_and_children',
                'position': u'footer',
            },
            {
                'path': u'/news',
                'path_snippet': u'For news and children (header)',
                'apply_to': u'context_and_children',
                'position': u'header',
            },
        ]
        settings.path_specific_code = records

        self.request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.assertTrue('For news and children (footer)' in self.portal.news())
        self.assertTrue('For news and children (header)' in self.portal.news())
        self.request.set('ACTUAL_URL', 'http://nohost/plone/news/home')
        self.assertTrue(
            'For news and children (footer)' in self.portal.news.home()
        )
        self.assertTrue(
            'For news and children (header)' in self.portal.news.home()
        )
        self.request.set('ACTUAL_URL', 'http://nohost/plone/news/subnews')
        self.assertTrue('SITE DEFAULT ANALYTICS' in self.portal.news.subnews())
        self.assertTrue(
            'DEFAULT ANALYTICS IN HEADER' in self.portal.news.subnews()
        )

    def test_apply_to_folder_and_children_with_new_folderish(self):
        self.markRequestWithLayer()
        settings = self.getSettings()
        settings.general_header_code = u'DEFAULT ANALYTICS IN HEADER'

        self.portal.invokeFactory(type_name='Folder', id='news', title="News")
        news = self.portal.news
        news.invokeFactory(
            type_name='News Item', id='real_news', title="A real news"
        )
        news.invokeFactory(
            type_name='Document', id='home', title="Homepage for news section"
        )

        records = [
            {
                'path': u'/news',
                'path_snippet': u'For news and children (footer)',
                'apply_to': u'context_and_children',
                'position': u'footer',
            },
            {
                'path': u'/news',
                'path_snippet': u'For news and children (header)',
                'apply_to': u'context_and_children',
                'position': u'header',
            },
        ]

        settings.path_specific_code = records
        settings.folderish_types = (u'Folder', u'News Item')

        self.request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.assertTrue('For news and children (footer)' in self.portal.news())
        self.assertTrue('For news and children (header)' in self.portal.news())
        self.request.set('ACTUAL_URL', 'http://nohost/plone/news/home')
        self.assertTrue(
            'For news and children (footer)' in self.portal.news.home()
        )
        self.assertTrue(
            'For news and children (header)' in self.portal.news.home()
        )
        self.request.set('ACTUAL_URL', 'http://nohost/plone/news/real_news')
        self.assertTrue(
            'SITE DEFAULT ANALYTICS' in self.portal.news.real_news()
        )
        self.assertTrue(
            'DEFAULT ANALYTICS IN HEADER' in self.portal.news.real_news()
        )

    def test_optout(self):
        self.markRequestWithLayer()
        settings = self.getSettings()
        settings.general_header_code = u'DEFAULT ANALYTICS IN HEADER'
        settings.respect_optout = True
        self.request.cookies = {'analytics-optout': 'true'}
        self.assertFalse('DEFAULT ANALYTICS IN HEADER' in self.portal())


class TestViewletPathCleanup(BaseTestCase):

    layer = ANALYTICS_PANEL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def getViewlet(self):
        return AnalyticsViewlet(self.portal, self.request, None, None)

    def test_add_starting_slash(self):
        viewlet = self.getViewlet()
        self.assertEquals(viewlet.cleanup_path('plone/foo'), '/plone/foo')

    def test_add_starting_portalid(self):
        viewlet = self.getViewlet()
        self.assertEquals(viewlet.cleanup_path('/foo'), '/plone/foo')

    def test_add_starting_portalid_and_slash(self):
        viewlet = self.getViewlet()
        self.assertEquals(viewlet.cleanup_path('foo'), '/plone/foo')

    def test_remove_trailing_slash(self):
        viewlet = self.getViewlet()
        self.assertEquals(viewlet.cleanup_path('/foo/bar/'), '/plone/foo/bar')

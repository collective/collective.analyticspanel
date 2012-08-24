# -*- coding: utf-8 -*-

from zope.component import getMultiAdapter

from collective.analyticspanel.testing import ANALYTICS_PANEL_INTEGRATION_TESTING
from collective.analyticspanel.pair_fields import ErrorCodeValuePair, SitePathValuePair

from collective.analyticspanel.browser.viewlet import AnalyticsViewlet

from base import BaseTestCase

class TestViewlet(BaseTestCase):

    layer = ANALYTICS_PANEL_INTEGRATION_TESTING

    def test_viewlet_registered(self):
        portal = self.layer['portal']
        request = self.layer['request']
        self.markRequestWithLayer()
        request.set('ACTUAL_URL', 'http://nohost/plone')
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
        request.set('ACTUAL_URL', 'http://nohost/plone')
        self.markRequestWithLayer()
        settings = self.getSettings()

        record = ErrorCodeValuePair()
        record.message = 'NotFound'
        record.message_snippet = u'You are in a NotFound page'

        settings.error_specific_code += (record,)
        request.set('error_type', 'NotFound')
        view = getMultiAdapter((portal, request), name=u"sharing")
        self.assertTrue('You are in a NotFound page' in view())

    def test_for_path(self):
        portal = self.layer['portal']
        portal.invokeFactory(type_name='Folder', id='news', title="News")
        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.markRequestWithLayer()
        settings = self.getSettings()

        record = SitePathValuePair()
        record.path = u'/news'
        record.path_snippet = u'You are in the News section'
        record.apply_to = u'subtree'
        settings.path_specific_code += (record,)

        self.assertTrue('You are in the News section' in portal.news())
        request.set('ACTUAL_URL', 'http://nohost/plone')
        self.assertFalse('You are in the News section' in portal())

    def test_most_specific_path_used(self):
        portal = self.layer['portal']
        portal.invokeFactory(type_name='Folder', id='news', title="News")
        portal.news.invokeFactory(type_name='Folder', id='subnews', title="Subfolder inside news")

        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.markRequestWithLayer()
        settings = self.getSettings()

        record1 = SitePathValuePair()
        record1.path = u'/news'
        record1.path_snippet = u'You are in the News section'
        record1.apply_to = u'subtree'
        record2 = SitePathValuePair()
        record2.path = u'/news/subnews'
        record2.path_snippet = u'You are in the Subnews section'
        record2.apply_to = u'subtree'
        settings.path_specific_code += (record1, record2)

        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.assertTrue('You are in the Subnews section' in portal.news.subnews())

    def test_hiding_code(self):
        portal = self.layer['portal']
        portal.invokeFactory(type_name='Folder', id='news', title="News")

        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.markRequestWithLayer()
        settings = self.getSettings()

        self.assertTrue('SITE DEFAULT ANALYTICS' in portal.news())

        record = SitePathValuePair()
        record.path = u'/news'
        record.path_snippet = u''
        record.apply_to = u'subtree'
        settings.path_specific_code += (record,)

        self.assertFalse('SITE DEFAULT ANALYTICS' in portal.news())

    def test_no_subtree_propagation(self):
        portal = self.layer['portal']
        portal.invokeFactory(type_name='Folder', id='news', title="News")

        request = self.layer['request']
        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.markRequestWithLayer()
        settings = self.getSettings()

        self.assertTrue('SITE DEFAULT ANALYTICS' in portal.news())

        record = SitePathValuePair()
        record.path = u'/news'
        record.path_snippet = u'Only for news'
        record.apply_to = u'context'
        settings.path_specific_code += (record,)

        self.assertTrue('Only for news' in portal.news())
        
        portal.news.invokeFactory(type_name='Folder', id='subnews', title="Subnews")
        request.set('ACTUAL_URL', 'http://nohost/plone/news/subnews')

        self.assertTrue('SITE DEFAULT ANALYTICS' in portal.news.subnews())

    def test_apply_to_folder_and_children(self):
        request = self.layer['request']
        self.markRequestWithLayer()
        settings = self.getSettings()

        portal = self.layer['portal']
        portal.invokeFactory(type_name='Folder', id='news', title="News")
        news = portal.news
        news.invokeFactory(type_name='Folder', id='subnews', title="Sub news")
        news.invokeFactory(type_name='Document', id='home', title="Homepage for news section")

        record = SitePathValuePair()
        record.path = u'/news'
        record.path_snippet = u'For news and children'
        record.apply_to = u'context_and_children'
        settings.path_specific_code += (record,)

        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.assertTrue('For news and children' in portal.news())
        request.set('ACTUAL_URL', 'http://nohost/plone/news/home')
        self.assertTrue('For news and children' in portal.news.home())
        request.set('ACTUAL_URL', 'http://nohost/plone/news/subnews')
        self.assertTrue('SITE DEFAULT ANALYTICS' in portal.news.subnews())

    def test_apply_to_folder_and_children_with_new_folderish(self):
        request = self.layer['request']
        self.markRequestWithLayer()
        settings = self.getSettings()

        portal = self.layer['portal']
        portal.invokeFactory(type_name='Folder', id='news', title="News")
        news = portal.news
        news.invokeFactory(type_name='News Item', id='real_news', title="A real news")
        news.invokeFactory(type_name='Document', id='home', title="Homepage for news section")

        record = SitePathValuePair()
        record.path = u'/news'
        record.path_snippet = u'For news and children'
        record.apply_to = u'context_and_children'
        settings.path_specific_code += (record,)
        settings.folderish_types = (u'Folder', u'News Item')

        request.set('ACTUAL_URL', 'http://nohost/plone/news')
        self.assertTrue('For news and children' in portal.news())
        request.set('ACTUAL_URL', 'http://nohost/plone/news/home')
        self.assertTrue('For news and children' in portal.news.home())
        request.set('ACTUAL_URL', 'http://nohost/plone/news/real_news')
        self.assertTrue('SITE DEFAULT ANALYTICS' in portal.news.real_news())


class TestViewletPathCleanup(BaseTestCase):
    
    layer = ANALYTICS_PANEL_INTEGRATION_TESTING
    
    def getViewlet(self):
        portal = self.layer['portal']
        request = self.layer['request']        
        return AnalyticsViewlet(portal, request, None, None)

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

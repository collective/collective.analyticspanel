# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema

from Products.CMFPlone import PloneMessageFactory as pmf

from collective.analyticspanel import messageFactory as _
from collective.analyticspanel.pair_fields import IErrorCodeValuePair, ISitePathValuePair
from collective.analyticspanel.pair_fields import PersistentObject

class IAnalyticsPanelLayer(Interface):
    """Browser layer interface for collective.analyticspanel"""

class IAnalyticsSettings(Interface):
    """Settings used in the control panel for analyticspanel
    """
    
    general_code = schema.Text(
            title=pmf(u"JavaScript for web statistics support"),
            description=pmf(u"For enabling web statistics support from external providers (for e.g. Google Analytics). "
                            u"Paste the code snippets provided. It will be included in the rendered HTML as entered near the end of the page."),
            default=u"",
            missing_value=u"",
            required=False,
    )

    error_specific_code = schema.Tuple(
            title=_(u'JavaScript to be included when an error message is get'),
            description=_('help_error_specific_code',
                          default=u"Replace default code included when an error message returned is "
                                   "one of the following values.\n"
                                   "For example: use \"NotFound\" for change JavaScript included inside NotFound page."),
            value_type=PersistentObject(IErrorCodeValuePair, title=_(u"Error message related snippet")),
            required=False,
            default=(),
            missing_value=(),
    )

    path_specific_code = schema.Tuple(
            title=_(u"JavaScript to be included inside specific site's paths"),
            description=_('help_path_specific_code',
                          default=u'Put there an absolute site path, and the statistics code you want to use '
                                  u'there instead of the default ones.\n'
                                  u'The most specific path will be used.\n'
                                  u'Example: /folder/subfolder'),
            value_type=PersistentObject(ISitePathValuePair, title=_(u"Site path related snippet")),
            required=False,
            default=(),
            missing_value=(),
    )


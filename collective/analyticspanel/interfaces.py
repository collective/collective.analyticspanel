# -*- coding: utf-8 -*-

import sys

from zope.interface import Interface
from zope import schema

from Products.CMFPlone import PloneMessageFactory as pmf

from collective.analyticspanel import messageFactory as _
from collective.analyticspanel.pair_fields import IErrorCodeValuePair, ISitePathValuePair
from collective.analyticspanel.pair_fields import PersistentObject

# This is awful, but plone.app.vocabularies version used on Plone 3 has a bug that will never be fixed
# See http://plone.293351.n2.nabble.com/Can-t-load-plone-app-vocabularies-ReallyUserFriendlyTypes-td7558326.html
# Please, remove this crappy thing as soon as Plone 3 support will be removed
if sys.version_info < (2, 6):
    # Plone 3
    FOLDER_TYPES_VALUESTYPE = schema.TextLine()
else:
    FOLDER_TYPES_VALUESTYPE = schema.Choice(vocabulary=u"plone.app.vocabularies.ReallyUserFriendlyTypes")

class IAnalyticsPanelLayer(Interface):
    """Browser layer interface for collective.analyticspanel"""


class IAnalyticsSettings(Interface):
    """Settings used in the control panel for analyticspanel: general panel
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


class IAnalyticsAdvancedSettings(Interface):
    """Settings used in the control panel for analyticspanel: advanced panel
    """

    folderish_types = schema.Tuple(
            title=_(u"Folderish types"),
            description=_("help_folderish_types",
                          default=u'Defines there which portal types must be treat as "folderish"'),
            required=False,
            value_type=FOLDER_TYPES_VALUESTYPE,
            default=(u'Folder',),
    )


class IAnalyticsSettingsSchema(IAnalyticsSettings, IAnalyticsAdvancedSettings):
    """Settings used in the control panel for analyticspanel: unified panel
    """

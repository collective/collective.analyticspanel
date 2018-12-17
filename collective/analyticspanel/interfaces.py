# -*- coding: utf-8 -*-
from collective.analyticspanel import messageFactory as _
from collective.z3cform.datagridfield.registry import DictRow
from zope import schema
from zope.interface import Interface

FOLDER_TYPES_VALUESTYPE = schema.Choice(
    vocabulary=u"plone.app.vocabularies.ReallyUserFriendlyTypes"
)


class IErrorCodeValuePair(Interface):
    message = schema.ASCIILine(title=_(u"Error message"), required=True)
    message_snippet = schema.SourceText(
        title=_(u"Code to include"), required=False
    )
    position = schema.Choice(
        title=_(u"Include code in..."),
        required=True,
        default=u'footer',
        vocabulary=u"collective.analyticspanel.vocabularies.positions",
    )


class ISitePathValuePair(Interface):
    path = schema.TextLine(title=_(u"Site path"), required=True)
    path_snippet = schema.SourceText(
        title=_(u"Code to include"), required=False
    )
    apply_to = schema.Choice(
        title=_(u"Apply rule to..."),
        description=_(
            'help_apply_to',
            default=u'Choose a policy for applying this rule.\n'
            u'When using "context and children" note that the rule will be '
            u'applied to the context and all non-folderish children.\n'
            u'This make sense only with folderish context.\n'
            u'See "Advanced settings" section for defining what is a folder '
            u'for your site.',
        ),
        required=True,
        default=u'subtree',
        vocabulary=u"collective.analyticspanel.vocabularies.apply_to_choices",
    )
    position = schema.Choice(
        title=_(u"Include code in..."),
        required=True,
        default=u'footer',
        vocabulary=u"collective.analyticspanel.vocabularies.positions",
    )


class IAnalyticsPanelLayer(Interface):
    """Browser layer interface for collective.analyticspanel"""


class IAnalyticsSettings(Interface):
    """Settings used in the control panel for analyticspanel: general panel
    """

    general_header_code = schema.Text(
        title=_(
            'general_header_code_label',
            default=u"JavaScript for web statistics support (in the header of the page)",
        ),
        description=_(
            'general_header_code_desciption',
            default=u"For enabling web statistics support from external providers (for e.g. Google Analytics). "
            u"Paste the code snippets provided. "
            u"It will be included in the rendered HTML as entered near the beginning of the page's BODY.\n"
            u"Commonly this is the best place where to put modern analytics code.",
        ),
        default=u"",
        missing_value=u"",
        required=False,
    )

    general_code = schema.Text(
        title=_(
            'general_footer_code_label',
            default=u"JavaScript for web statistics support (in the footer of the page)",
        ),
        description=_(
            'general_footer_code_desciption',
            u"For enabling web statistics support from external providers (for e.g. Google Analytics). "
            u"Paste the code snippets provided.\n"
            u"It will be included in the rendered HTML as entered near the end of the page.\n"
            u"Historically Plone put it's analytics code here and this can still be the best place for "
            u"old analytics software that block the page rendering.",
        ),
        default=u"",
        missing_value=u"",
        required=False,
    )

    error_specific_code = schema.List(
        title=_(u'JavaScript to be included when an error message is get'),
        description=_(
            'help_error_specific_code',
            default=u"Replace default code included when an error message returned is "
            "one of the following values.\n"
            "For example: use \"NotFound\" for change JavaScript included inside NotFound page.",
        ),
        value_type=DictRow(
            title=_(u"Error message related snippet"),
            schema=IErrorCodeValuePair,
        ),
        required=False,
    )

    path_specific_code = schema.List(
        title=_(u"JavaScript to be included inside specific site's paths"),
        description=_(
            'help_path_specific_code',
            default=u'Put there an absolute site path, and the statistics code you want to use '
            u'there instead of the default ones.\n'
            u'The most specific path will be used.\n'
            u'Example: /folder/subfolder',
        ),
        value_type=DictRow(
            schema=ISitePathValuePair, title=_(u"Site path related snippet")
        ),
        required=False,
    )

    respect_donottrack = schema.Bool(
        title=_(u'Respect "Do Not Track" browser setting'),
        description=_(
            'help_respect_donottrack',
            default=u"Do not send analytics if user activated the DNT header.\n"
            u"See https://en.wikipedia.org/wiki/Do_Not_Track",
        ),
        default=False,
    )

    respect_optout = schema.Bool(
        title=_(u'Respect \"analytics-optout\" cookie'),
        description=_(
            'help_respect_optout',
            default=u"If a cookie named \"analytics-optout\" exists and is valued \"true\" "
            u"do not send analytics data.",
        ),
        default=False,
    )


class IAnalyticsAdvancedSettings(Interface):
    """Settings used in the control panel for analyticspanel: advanced panel
    """

    folderish_types = schema.Tuple(
        title=_(u"Folderish types"),
        description=_(
            "help_folderish_types",
            default=u'Defines there which portal types must be treat as "folderish"',
        ),
        required=False,
        value_type=FOLDER_TYPES_VALUESTYPE,
        default=(u'Folder',),
    )


class IAnalyticsSettingsSchema(IAnalyticsSettings, IAnalyticsAdvancedSettings):
    """Settings used in the control panel for analyticspanel: unified panel
    """

# -*- coding: utf-8 -*-

from collective.analyticspanel import messageFactory as _
from plone.registry.field import PersistentField
from z3c.form.object import registerFactoryAdapter
from zope import schema
from zope.interface import Interface, implements


class IErrorCodeValuePair(Interface):
    message = schema.ASCIILine(title=_(u"Error message"), required=True)
    message_snippet = schema.SourceText(title=_(u"Code to include"), required=False)
    position = schema.Choice(title=_(u"Include code in..."),
                             required=True,
                             default=u'footer',
                             vocabulary=u"collective.analyticspanel.vocabularies.positions")


class ErrorCodeValuePair(object):
    implements(IErrorCodeValuePair)

    def __init__(self, message=None, message_snippet=None, position='footer'):
        self.message = message
        self.message_snippet = message_snippet
        self.position = position


class ISitePathValuePair(Interface):
    path = schema.TextLine(title=_(u"Site path"), required=True)
    path_snippet = schema.SourceText(title=_(u"Code to include"), required=False)
    apply_to = schema.Choice(title=_(u"Apply rule to..."),
                             description=_('help_apply_to',
                                           default=u'Choose a policy for applying this rule.\n'
                                                   u'When using "context and children" note that the rule will be '
                                                   u'applied to the context and all non-folderish children.\n'
                                                   u'This make sense only with folderish context.\n'
                                                   u'See "Advanced settings" section for defining what is a folder '
                                                   u'for your site.'),
                             required=True,
                             default=u'subtree',
                             vocabulary=u"collective.analyticspanel.vocabularies.apply_to_choices")
    position = schema.Choice(title=_(u"Include code in..."),
                             required=True,
                             default=u'footer',
                             vocabulary=u"collective.analyticspanel.vocabularies.positions")


class SitePathValuePair(object):
    implements(ISitePathValuePair)

    def __init__(self, path=None, path_snippet=None, apply_to=None, position='footer'):
        self.path = path
        self.path_snippet = path_snippet
        self.apply_to = apply_to
        self.position = position


class PersistentObject(PersistentField, schema.Object):
    pass


registerFactoryAdapter(IErrorCodeValuePair, ErrorCodeValuePair)
registerFactoryAdapter(ISitePathValuePair, SitePathValuePair)


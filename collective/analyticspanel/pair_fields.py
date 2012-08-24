# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface, implements

from z3c.form.object import registerFactoryAdapter

from plone.registry.field import PersistentField

from collective.analyticspanel import messageFactory as _

class IErrorCodeValuePair(Interface):
    message = schema.ASCIILine(title=_(u"Error message"), required=True)
    message_snippet = schema.SourceText(title=_(u"Code to include"), required=False)

class ErrorCodeValuePair(object):
    implements(IErrorCodeValuePair)

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


class SitePathValuePair(object):
    implements(ISitePathValuePair)

class PersistentObject(PersistentField, schema.Object):
    pass

registerFactoryAdapter(IErrorCodeValuePair, ErrorCodeValuePair)
registerFactoryAdapter(ISitePathValuePair, SitePathValuePair)


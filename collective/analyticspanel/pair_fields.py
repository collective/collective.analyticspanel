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
    apply_to_subsection = schema.Bool(title=_(u"Apply to whole subtree"),
                                              description=_(u"If checked, the rules will be applied also to contents "
                                                            u"below that level"),
                                              required=False, default=True)

class SitePathValuePair(object):
    implements(ISitePathValuePair)

class PersistentObject(PersistentField, schema.Object):
    pass

registerFactoryAdapter(IErrorCodeValuePair, ErrorCodeValuePair)
registerFactoryAdapter(ISitePathValuePair, SitePathValuePair)


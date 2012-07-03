# -*- coding: utf-8 -*-

from persistent import Persistent

from zope import schema
from zope.schema.interfaces import IObject
from zope.schema.fieldproperty import FieldProperty

from zope.interface import Interface, implements
import zope.interface
import zope.component

from z3c.form.object import registerFactoryAdapter

from plone.registry.field import PersistentCollectionField, PersistentField
from plone.registry.interfaces import IPersistentField
from plone.registry.fieldfactory import persistentFieldAdapter

from collective.analyticspanel import messageFactory as _

class IErrorCodeValuePair(Interface):
    message = schema.ASCIILine(title=_(u"Error message"), required=True)
    message_snippet = schema.SourceText(title=_(u"Code to include"), required=False)

class ErrorCodeValuePair(object):
    implements(IErrorCodeValuePair)

class ISitePathValuePair(Interface):
    path = schema.TextLine(title=_(u"Site path"), required=True)
    path_snippet = schema.SourceText(title=_(u"Code to include"), required=False)

class SitePathValuePair(object):
    implements(ISitePathValuePair)

class PersistentObject(PersistentField, schema.Object):
    pass

registerFactoryAdapter(IErrorCodeValuePair, ErrorCodeValuePair)
registerFactoryAdapter(ISitePathValuePair, SitePathValuePair)


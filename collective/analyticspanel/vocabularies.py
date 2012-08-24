# -*- coding: utf-8 -*-

from zope.interface import implements

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    # Plone 4.1+
    from zope.schema.interfaces import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.analyticspanel import messageFactory as _

class ApplyToChoicesVocabulary(object):
    """Vocabulary for the apply_to field
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        
        terms = [SimpleTerm(u'subtree', _(u'...to the whole subtree')),
                 SimpleTerm(u'context', _(u'...only to the context')),
                 SimpleTerm(u'context_and_children', _(u'...to the context and non-folderish children')),
                 ]
        return SimpleVocabulary(terms)

applyToChoicesVocabularyFactory = ApplyToChoicesVocabulary()
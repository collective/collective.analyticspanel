# -*- coding: utf-8 -*-

from zope.interface import implementer

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.analyticspanel import messageFactory as _


@implementer(IVocabularyFactory)
class ApplyToChoicesVocabulary(object):
    """Vocabulary for the apply_to field
    """

    def __call__(self, context):

        terms = [SimpleTerm(u'subtree', u'subtree', _('scope_whole_subtree',
                                                      default=u'...to the whole subtree')),
                 SimpleTerm(u'context', u'context', _('scope_context_only',
                                                      default=u'...only to the context')),
                 SimpleTerm(u'context_and_children', u'context_and_children',
                            _('scope_context_and_not_folderish',
                              default=u'...to the context and non-folderish children')),
                 ]
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class SnippetPositionsVocabulary(object):
    """Vocabulary for the position of the snippet
    """

    def __call__(self, context):

        terms = [SimpleTerm(u'header', u'header', _('position_header',
                                                      default=u'...in the header of the page')),
                 SimpleTerm(u'footer', u'footer', _('position_footer',
                              default=u'...in the footer of the page')),
                 ]
        return SimpleVocabulary(terms)


applyToChoicesVocabularyFactory = ApplyToChoicesVocabulary()
snippetPositionVocabularyFactory = SnippetPositionsVocabulary()

# -*- coding: utf-8 -*-
""" Portal catalog indexers """

from five import grok

from plone.indexer import indexer

from collective.roster.behaviors.interfaces import (
    IHasRelatedPersons,
    IRelatedPersons,
    IGroupsAsSubjects
)
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


@indexer(IHasRelatedPersons)
def RelatedPersonsIndexer(context):
    """ Indexes related person UUIDs to be searched from the catalog """
    adapted = IRelatedPersons(context)
    bound = IRelatedPersons["related_persons"].bind(adapted)
    return bound.get(adapted)

grok.global_adapter(RelatedPersonsIndexer, name="related_persons")


@indexer(IGroupsAsSubjects)
def subject(context):
    vocabulary_factory = getUtility(IVocabularyFactory,
                                    name="collective.roster.localgroups")
    vocabulary = vocabulary_factory(context)
    group_terms_filter = lambda term: term.value in context.groups

    terms = filter(group_terms_filter, vocabulary)

    groups = map(lambda term: term.title.encode("utf-8"), terms)

    return context.subject + tuple(groups)
grok.global_adapter(subject, name="Subject")

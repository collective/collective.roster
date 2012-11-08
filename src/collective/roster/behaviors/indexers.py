# -*- coding: utf-8 -*-
""" Portal catalog indexers """

from five import grok

from plone.indexer import indexer

from collective.roster.behaviors.interfaces import (
    IHasRelatedPersons,
    IRelatedPersons
)


@indexer(IHasRelatedPersons)
def RelatedPersonsIndexer(context):
    """ Indexes related person UUIDs to be searched from the catalog """
    adapted = IRelatedPersons(context)
    bound = IRelatedPersons["related_persons"].bind(adapted)
    return bound.get(adapted)

grok.global_adapter(RelatedPersonsIndexer, name="related_persons")

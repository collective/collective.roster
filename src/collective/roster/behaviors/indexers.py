from collective.roster.interfaces import IHasRelatedPersons
from collective.roster.behaviors.interfaces import IRelatedPersons
from five import grok
from plone.indexer import indexer


@grok.adapter(IHasRelatedPersons, name="related_persons")
@indexer(IHasRelatedPersons)
def RelatedPersonsIndexer(context):
    """ create index from UUID list so we can search catalog with it"""
    return IRelatedPersons(context).related_persons

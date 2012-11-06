from collective.roster.behaviors.interfaces import IHasRelatedPersons
from collective.roster.behaviors.interfaces import IRelatedPersons
from five import grok
from plone.indexer import indexer


@indexer(IHasRelatedPersons)
def RelatedPersonsIndexer(context):
    """ create index from UUID list so we can search catalog with it"""
    adapted = IRelatedPersons(context)
    bound = IRelatedPersons["related_persons"].bind(adapted)
    return bound.get(adapted)

grok.global_adapter(RelatedPersonsIndexer, name="related_persons")

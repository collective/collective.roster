# -*- coding: utf-8 -*-
from collective.roster.behaviors.interfaces import IGroups
from collective.roster.behaviors.interfaces import IGroupsAsSubjects
from zope.component import adapter
from zope.component import getUtility
from zope.component.interfaces import IObjectEvent
from zope.schema.interfaces import IVocabularyFactory


# noinspection PyUnusedLocal
@adapter(IGroupsAsSubjects, IObjectEvent)
def append_groups_into_subjects(ob, event=None):

    vocabulary_factory = getUtility(IVocabularyFactory,
                                    name='collective.roster.localgroups')
    vocabulary = vocabulary_factory(ob)

    subjects = set(getattr(ob, 'subject', None) or ())
    subjects = list(subjects.intersection(
        set(filter(vocabulary.__contains__, subjects))))

    groups = [term.title.encode('utf-8', 'ignore')
              for term in vocabulary
              if term.value in IGroups(ob).groups]

    ob.subject = tuple(set(subjects + groups))
    ob.reindexObject(idxs=('Subject',))

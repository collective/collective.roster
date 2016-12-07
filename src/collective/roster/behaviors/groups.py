# -*- coding: utf-8 -*-
from collective.roster.behaviors.interfaces import IGroups
from collective.roster.behaviors.interfaces import IGroupsProvider
from collective.roster.behaviors.interfaces import IHasGroups
from collective.roster.behaviors.interfaces import IProvidesGroups
from collective.roster.roster import PersonnelListing
from collective.roster.utils import parents
from collective.roster.utils import sortable_title
from operator import methodcaller
from plone.i18n.normalizer import IIDNormalizer
from plone.indexer import indexer
from plone.memoize import view
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IGroupsProvider)
@implementer(IGroups)
class Groups(object):
    """Attribute storage
    """
    def __init__(self, context):
        self.context = context

    def get_groups(self):
        return getattr(self.context, 'groups', [])

    def set_groups(self, groups):
        if groups is None:
            groups = []
        setattr(self.context, 'groups', groups)

    groups = property(get_groups, set_groups)


# noinspection PyUnusedLocal
@indexer(Interface)
def skipIndex(ob):
    raise AttributeError


@indexer(IHasGroups)
def indexRosterGroups(ob):
    return IGroups(ob).groups


@implementer(IVocabularyFactory)
class LocalGroupsVocabulary(object):
    """Return a new context bound vocabulary, which returns the
    groups defined in the nearest parent roster
    """
    def __call__(self, context):
        groups = []
        roster = None
        normalizer = getUtility(IIDNormalizer)
        for parent in tuple(parents(context, iface=IProvidesGroups)):
            roster = parent
            break
        for group in (getattr(roster, 'groups', ()) or ()):
            if group is None:
                continue
            if '|' in group:
                value, title = group.split('|', 1)
            else:
                value = title = group
            groups.append(
                SimpleTerm(value,
                           token=normalizer.normalize(group),
                           title=title)
            )
        return SimpleVocabulary(groups)


class PersonnelGroupListing(PersonnelListing):

    sortOn = None

    def __init__(self, context, request, group):
        super(PersonnelGroupListing, self).__init__(context, request)
        self.group = group

    @property
    def title(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name='collective.roster.localgroups')
        vocabulary = vocabulary_factory(self.context)
        term = vocabulary.getTerm(self.group)
        return term.title

    @property
    def anchorTitle(self):
        normalizer = getUtility(IIDNormalizer)
        return normalizer.normalize(self.title)

    # Personnel values property, which provides and objects for all the persons
    # with the same group as the currently rendered personnel table
    @property
    def values(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name='collective.roster.localgroups')
        vocabulary = vocabulary_factory(self.context)
        term = vocabulary.getTerm(self.group)

        pc = getToolByName(self.context, 'portal_catalog')
        brains = pc(
            path='/'.join(self.context.getPhysicalPath()),
            roster_groups=[term.value]
        )
        values = map(methodcaller('getObject'), brains)

        sorted_values = sorted(values, key=sortable_title)
        return sorted_values


class GroupsView(BrowserView):
    @property
    @view.memoize
    def tables(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name='collective.roster.localgroups')
        vocabulary = vocabulary_factory(self.context)

        tables = [
            PersonnelGroupListing(self.context, self.request, group)
            for group in [term.value for term in vocabulary]
        ]

        for table in tables:
            table.update()

        return tables

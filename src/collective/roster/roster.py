# -*- coding: utf-8 -*-
"""Personnel roster"""

from five import grok

from zope.component import getMultiAdapter, getUtility
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


from z3c.table.interfaces import IValues, IColumn
from z3c.table import table, column

from Products.CMFCore.utils import getToolByName

from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.i18n.normalizer.interfaces import IIDNormalizer

from collective.roster.interfaces import IPersonnelListing, IPerson, IRoster
from collective.roster.utils import getFirstParent


from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
_ = ZopeMessageFactory("collective.roster")


class LocalGroupsVocabulary(grok.GlobalUtility):
    """Local roster groups vocabulary"""

    grok.provides(IVocabularyFactory)
    grok.name("collective.roster.localgroups")

    def __call__(self, context):
        groups = []
        normalizer = getUtility(IIDNormalizer)
        roster = getFirstParent(context, IRoster)
        for group in getattr(roster, "groups", ()):
            groups.append(
                SimpleTerm(group,
                           token=normalizer.normalize(group),
                           title=group)
            )
        return SimpleVocabulary(groups)


class View(grok.View):
    """Personnel listing"""

    grok.context(IRoster)
    grok.require("zope2.View")
    grok.name("view")

    def update(self):
        from zope.viewlet.interfaces import IViewletManager
        self.viewlets = getMultiAdapter(
            (self.context, self.request, self),
            IViewletManager, name="collective.roster.rosterviewlets")
        self.viewlets.update()


class RosterViewlets(OrderedViewletManager, grok.ViewletManager):
    grok.context(IRoster)
    grok.name("collective.roster.rosterviewlets")


class ListingViewlet(grok.Viewlet):
    """Personnel listing"""

    grok.viewletmanager(RosterViewlets)
    grok.context(IRoster)
    grok.name("collective.roster.rosterviewlets.listing")

    def __init__(self, *args, **kwargs):
        super(ListingViewlet, self).__init__(*args, **kwargs)
        self.tables = map(
            lambda group: PersonnelListing(self.context, self.request, group),
            self.context.groups)

    def update(self):
        super(ListingViewlet, self).update()
        for table in self.tables:
            table.update()


class PersonnelListing(table.Table):
    """Personnel listing"""
    grok.implements(IPersonnelListing)

    # CSS
    cssClasses = {'table': u"listing", 'td': u"notDraggable"}
    cssClassEven = u"even"
    cssClassOdd = u"odd"

    # Sort
    sortOn = None  # (z3c.table expects sortOn to be either None, 0 or column
                   # order aware id[table-column-idx])

    # Batching
    batchProviderName = "plonebatch"
    batchSize = 10
    startBatchingAt = 10

    @property
    def title(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name="collective.roster.localgroups")
        vocabulary = vocabulary_factory(self.context)
        term = vocabulary.getTerm(self.group)
        return term.title

    def __init__(self, context, request, group):
        super(PersonnelListing, self).__init__(context, request)
        self.group = group

    def getBatchSize(self):
        return max(int(self.request.get(self.prefix + '-batchSize',
                                        self.batchSize)), 1)


class PersonnelValues(grok.MultiAdapter):
    """Personnel values"""

    grok.provides(IValues)
    grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)

    def __init__(self, context, request, table):
        self.context = context
        self.request = request
        self.table = table

    @property
    def values(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name="collective.roster.localgroups")
        vocabulary = vocabulary_factory(self.context)
        term = vocabulary.getTerm(self.table.group)

        pc = getToolByName(self.context, "portal_catalog")
        values = pc(path="/".join(self.context.getPhysicalPath()),
                    object_provides=IPerson.__identifier__,
                    Subject=(term.value,))

        return values


# class TitleColumn(grok.MultiAdapter, column.GetAttrColumn):
#     """Title column"""
#
#     grok.provides(IColumn)
#     grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
#     grok.name("collective.roster.personnellisting.title")
#
#     weight = 100
#
#     header = _(u"Title")
#     attrName = "Title"


class TitleColumn(grok.MultiAdapter, column.LinkColumn):
    """Title column"""

    grok.provides(IColumn)
    grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
    grok.name("collective.roster.personnellisting.title")

    weight = 100

    header = _(u"Title")

    def getLinkURL(self, item):
        return item.getURL()

    def getLinkContent(self, item):
        title = item.Title
        if type(title) != unicode:
            title = unicode(title, u"utf-8")
        return title

# -*- coding: utf-8 -*-
"""Personnel roster, which contains and displays person information"""

from five import grok

from zope.component import (
    getGlobalSiteManager,
    getMultiAdapter,
    getUtility
)

from zope.publisher.interfaces.browser import IBrowserRequest

from zope.schema.interfaces import (
    IVocabularyFactory,
    IList
)
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from z3c.form.datamanager import AttributeField
from z3c.table.interfaces import (
    IValues,
    IColumn
)
from z3c.table import (
    table,
    column
)

from Products.CMFCore.utils import getToolByName

from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.i18n.normalizer.interfaces import IIDNormalizer

from collective.roster.interfaces import IPersonnelListing, IPerson, IRoster
from collective.roster.utils import getFirstParent


from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
_ = ZopeMessageFactory("collective.roster")


class LocalGroupsVocabulary(grok.GlobalUtility):
    """Returns a new context bound vocabulary, which returns the groups defined
    in the nearest parent roster"""

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


class DisplayColumnsVocabulary(grok.GlobalUtility):
    """Returns a new context indepeneent vocabulary, which return all the table
    columns registered for the roster interface"""

    grok.provides(IVocabularyFactory)
    grok.name("collective.roster.columns")

    def _isColumnAdapter(self, obj):
        return obj.required == (IRoster, IBrowserRequest, IPersonnelListing)\
            and obj.provided == IColumn

    def __call__(self, context):
        gsm = getGlobalSiteManager()
        adapters = gsm.registeredAdapters()
        columns = filter(self._isColumnAdapter, adapters)
        terms = map(lambda x: SimpleTerm(x.name, x.name, x.factory.header),
                    columns)
        return SimpleVocabulary(terms)


class RosterDataManager(grok.MultiAdapter, AttributeField):
    """z3c.form datamanager, which reverts the behavior of display columns
    field to store hidden columns instead"""

    grok.adapts(IRoster, IList)

    def _isColumnAdapter(self, obj):
        return obj.required == (IRoster, IBrowserRequest, IPersonnelListing)\
            and obj.provided == IColumn

    def _getAllColumns(self):
        gsm = getGlobalSiteManager()
        adapters = gsm.registeredAdapters()
        columns = filter(self._isColumnAdapter, adapters)
        return map(lambda x: x.name, columns)

    def get(self):
        value = super(RosterDataManager, self).get()
        if self.field.__name__ == "columns_hidden" and value is not None:
            columns = self._getAllColumns()  # XXX: could use vocab instead
            selection = [] if value is None else value  # value can be None
            value = filter(lambda x: x not in selection, columns)
        return value

    def set(self, value):
        if self.field.__name__ == "columns_hidden":
            columns = self._getAllColumns()  # XXX: could use vocab instead
            selection = [] if value is None else value  # value can be None
            value = filter(lambda x: x not in selection, columns)
        return super(RosterDataManager, self).set(value)


class View(grok.View):
    """Personnel listing view, which is composed using its own viewlet
    manager to make it extensible and configurable"""

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
    """The default personnel listing viewlet, which generates a personnel
    listing table per defined group in personnel roster"""

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
    """Personnel listing table, which can be exteneded with custom columns"""
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
    def setUpColumns(self):
        hidden = getattr(self.context, "columns_hidden", [])
        cols = super(PersonnelListing, self).setUpColumns()
        return filter(lambda x: x.__name__ not in hidden, cols)


class PersonnelValues(grok.MultiAdapter):
    """Personnel values adapter, which provides catalog brains for all
    the persons with the same group as the currently rendered personnel
    listing table under the current personnel roster"""

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
    """Column, which renders person's full name with salutation"""

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

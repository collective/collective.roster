# -*- coding: utf-8 -*-
"""Personnel roster"""

from five import grok

from zope.component import getMultiAdapter
from zope.publisher.interfaces.browser import IBrowserRequest

from z3c.table.interfaces import IValues, IColumn
from z3c.table import table, column

from Products.CMFCore.utils import getToolByName

from plone.app.viewletmanager.manager import OrderedViewletManager

from jyu.roster.interfaces import IPersonnelListing
from jyu.roster.schemas import IPerson, IRoster

from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
_ = ZopeMessageFactory("jyu.roster")


class View(grok.View):
    """Personnel listing"""

    grok.context(IRoster)
    grok.require("zope2.View")
    grok.name("view")

    def update(self):
        from zope.viewlet.interfaces import IViewletManager
        self.viewlets = getMultiAdapter(
            (self.context, self.request, self),
            IViewletManager, name="jyu.roster.rosterviewlets")
        self.viewlets.update()


class RosterViewlets(OrderedViewletManager, grok.ViewletManager):
    grok.context(IRoster)
    grok.name("jyu.roster.rosterviewlets")


class ListingViewlet(grok.Viewlet):
    """Personnel listing"""

    grok.viewletmanager(RosterViewlets)
    grok.context(IRoster)
    grok.name("jyu.roster.rosterviewlets.listing")

    def __init__(self, *args, **kwargs):
        super(ListingViewlet, self).__init__(*args, **kwargs)
        self.table = PersonnelListing(self.context, self.request)

    def update(self):
        super(ListingViewlet, self).update()
        self.table.update()


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
        pc = getToolByName(self.context, "portal_catalog")
        values = pc(path="/".join(self.context.getPhysicalPath()),
                    object_provides=IPerson.__identifier__)
        return values


# class TitleColumn(grok.MultiAdapter, column.GetAttrColumn):
#     """Title column"""
#
#     grok.provides(IColumn)
#     grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
#     grok.name("jyu.roster.personnellisting.title")
#
#     weight = 100
#
#     header = _(u"Title")
#     attrName = "Title"


class TitleColumn(grok.MultiAdapter, column.LinkColumn):
    """Title column"""

    grok.provides(IColumn)
    grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
    grok.name("jyu.roster.personnellisting.title")

    weight = 100

    header = _(u"Title")

    def getLinkURL(self, item):
        return item.getURL()

    def getLinkContent(self, item):
        return item.Title

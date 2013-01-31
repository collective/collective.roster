# -*- coding: utf-8 -*-
"""Roster (aka. personnel directory)
"""

from five import grok

from zope.component import (
    getGlobalSiteManager,
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

from plone.i18n.normalizer.interfaces import IIDNormalizer

from collective.roster.interfaces import (
    IPersonnelListing,
    IPerson,
    IRoster
)
from collective.roster.behaviors.interfaces import (
    IContactInfo,
    IOfficeInfo

)
from collective.roster.utils import getFirstParent


from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
_ = ZopeMessageFactory("collective.roster")


class LocalGroupsVocabulary(grok.GlobalUtility):
    """ Returns a new context bound vocabulary, which returns the
    groups defined in the nearest parent roster """

    grok.provides(IVocabularyFactory)
    grok.name("collective.roster.localgroups")

    def __call__(self, context):
        groups = []
        normalizer = getUtility(IIDNormalizer)
        roster = getFirstParent(context, IRoster)
        for group in getattr(roster, "groups", ()):
            if "|" in group:
                value, title = group.split("|", 1)
            else:
                value = title = group
            groups.append(
                SimpleTerm(value,
                           token=normalizer.normalize(group),
                           title=title)
            )
        return SimpleVocabulary(groups)


class DisplayColumnsVocabulary(grok.GlobalUtility):
    """ Returns a new context independent vocabulary, which return all the
    table columns registered for the roster interface """

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
    """ z3c.form datamanager, which reverts the behavior of display columns
    field to store hidden columns instead """

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
    """ Personnel listing view, which is composed using its own viewlet manager
    to make it extensible and configurable """

    grok.context(IRoster)
    grok.require("zope2.View")
    grok.name("view")

    def __init__(self, context, request):
        super(View, self).__init__(context, request)

        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name="collective.roster.localgroups")
        vocabulary = vocabulary_factory(self.context)
        self.tables = map(
            lambda group: PersonnelGroupListing(self.context, self.request,
                                                group),
            map(lambda term: term.value, vocabulary)
        )

    def update(self):
        super(View, self).update()
        for table in self.tables:
            table.update()


class AlphaView(grok.View):
    grok.context(IRoster)
    grok.require("zope2.View")
    grok.name("alphaview")

    def __init__(self, context, request):
        super(AlphaView, self).__init__(context, request)
        self.table = PersonnelAlphaListing(self.context, self.request)

    def update(self):
        super(AlphaView, self).update()
        self.table.update()

    #def render(self):
        #table = self.table.render()
        #output = ""
        #for alpha in self.table.alpha:
            #output += """<a href="#%s">%s</a>""" % (alpha, alpha)
        #return output + table


class PersonnelListing(table.Table):
    """ Personnel listing table, which can be exteneded with custom columns """
    grok.implements(IPersonnelListing)

    title = u""

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

    def setUpColumns(self):
        bound = IRoster["columns_hidden"].bind(self.context)
        hidden = bound.get(self.context) or []
        cols = super(PersonnelListing, self).setUpColumns()
        return filter(lambda x: x.__name__ not in hidden, cols)

    @property
    def values(self):
        pc = getToolByName(self.context, "portal_catalog")
        values = pc(
            path="/".join(self.context.getPhysicalPath()),
            object_provides=IPerson.__identifier__
        )

        return values


class PersonnelAlphaListing(PersonnelListing):

    cssClasses = {'table': u"listing", 'td': u"nosort notDraggable"}

    alpha = []
    @property
    def values(self):
        values = super(PersonnelAlphaListing, self).values
        sort_by_title = lambda x, y: cmp(x.Title.lower(), y.Title.lower())
        return sorted(values, cmp=sort_by_title)

    def update(self):
        super(PersonnelAlphaListing, self).update()
        self.alpha = []


class AlphaColumn(grok.MultiAdapter, column.Column):

    grok.provides(IColumn)
    grok.adapts(IRoster, IBrowserRequest, PersonnelAlphaListing)
    grok.name("collective.roster.personnellisting.alpha")

    weight = 0

    header = _(u"#")

    def renderCell(self, item):
        obj = item.getObject()
        alpha = obj.last_name[0] if len(obj.last_name) else None
        if not self.table.alpha or alpha != self.table.alpha[-1]:
            alpha = alpha.lower()
            self.table.alpha.append(alpha)
            return u"""<a name="%s">%s</a>""" % (alpha, alpha)
        else:
            return u""


class PersonnelGroupListing(PersonnelListing):

    def __init__(self, context, request, group):
        super(PersonnelGroupListing, self).__init__(context, request)
        self.group = group

    @property
    def title(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name="collective.roster.localgroups")
        vocabulary = vocabulary_factory(self.context)
        term = vocabulary.getTerm(self.group)
        return term.title

    """ Personnel values adapter, which provides catalog brains for all the
    persons with the same group as the currently rendered personnel listing
    table under the current personnel roster """
    @property
    def values(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name="collective.roster.localgroups")
        vocabulary = vocabulary_factory(self.context)
        term = vocabulary.getTerm(self.table.group)

        pc = getToolByName(self.context, "portal_catalog")
        values = pc(
            path="/".join(self.context.getPhysicalPath()),
            object_provides=IPerson.__identifier__,
            Subject=(term.title.encode("utf-8"),)  # are indexed by titles
        )

        return values


class TitleColumn(grok.MultiAdapter, column.LinkColumn):
    """ Column, which renders person's full name with salutation """

    grok.provides(IColumn)
    grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
    grok.name("collective.roster.personnellisting.title")

    weight = 99

    header = _(u"Title")

    def getLinkURL(self, item):
        return item.getURL()

    def getLinkContent(self, item):
        obj = item.getObject()
        title = u"%s %s" % (obj.last_name, obj.first_name)
        if type(title) != unicode:
            title = unicode(title, u"utf-8")
        return title


class SalutationColumn(grok.MultiAdapter, column.Column):
    """ Column which renders person's salutation """

    grok.provides(IColumn)
    grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
    grok.name("collective.roster.personnellisting.salutation")

    weight = 100

    header = _(u"Salutation")

    def renderCell(self, item):
        return item.getObject().salutation


class RoomColumn(grok.MultiAdapter, column.Column):
    """ Column, which renders person's room """

    grok.provides(IColumn)
    grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
    grok.name("collective.roster.personnellisting.room")

    weight = 101

    header = _(u"Room")

    def renderCell(self, item):
        adapter = IOfficeInfo(item.getObject(), None)
        if adapter:
            return getattr(adapter, "room", u"")
        return u""


class PhoneNumberColumn(grok.MultiAdapter, column.Column):
    """ Column, which renders person's phone number """

    grok.provides(IColumn)
    grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
    grok.name("collective.roster.personnellisting.phone_number")

    weight = 102

    header = _(u"Phone number")

    def renderCell(self, item):
        adapter = IContactInfo(item.getObject(), None)
        if adapter:
            return getattr(adapter, "phone_number", u"")
        return u""


class EmailColumn(grok.MultiAdapter, column.Column):
    """ Column, which renders person's email address """

    grok.provides(IColumn)
    grok.adapts(IRoster, IBrowserRequest, IPersonnelListing)
    grok.name("collective.roster.personnellisting.email")

    weight = 103

    header = _(u"Email")

    def renderCell(self, item):
        adapter = IContactInfo(item.getObject(), None)
        if adapter:
            return getattr(adapter, "email", u"")
        return u""

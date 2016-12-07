# -*- coding: utf-8 -*-
"""Personnel roster (to contain and display persons)
"""
from collective.roster import _
from collective.roster.interfaces import IPerson
from collective.roster.interfaces import IPersonnelListing
from collective.roster.interfaces import IRoster
from collective.roster.utils import parents
from collective.roster.utils import sortable_title
from plone import api
from plone.memoize import view
from Products.CMFCore.WorkflowCore import WorkflowException
from z3c.table import column
from z3c.table import table
from z3c.table.interfaces import IColumn
from z3c.table.table import getWeight
from zope.component import adapter
from zope.component import getAdapters
from zope.component import getUtility
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import sys


@implementer(IRoster)
class MockRoster(object):
    pass


@implementer(IVocabularyFactory)
class DisplayColumnsVocabulary(object):
    """Return a new context independent vocabulary, which return all the
    table columns registered for the roster interface
    """
    # noinspection PyUnusedLocal
    def __call__(self, context=None):
        terms = []
        for roster in parents(context, iface=IRoster):
            context = roster
        if not IRoster.providedBy(context):
            context = MockRoster()
        request = api.portal.getRequest()
        tbl = PersonnelListing(context, request)
        for name, col in getAdapters((context, request, tbl), IColumn):
            terms.append(SimpleTerm(name, name, col.header))
        return SimpleVocabulary(terms)


class ColumnDisplaySortKey(object):

    def __init__(self, columns_display):
        self.columns_display = columns_display

    def __call__(self, col):
        if col.__name__ in self.columns_display:
            return self.columns_display.index(col.__name__)
        else:
            return getWeight(col)


@implementer(IPersonnelListing)
class PersonnelListing(table.Table):
    """Personnel listing table, which can be extended with custom columns
    """
    title = u''

    # CSS
    cssClasses = {'table': u'listing roster', 'td': u'notDraggable'}
    cssClassEven = u'even'
    cssClassOdd = u'odd'

    # Sort (z3c.table expects sortOn to be either None, 0 or column index
    sortOn = 1

    # Batching
    batchProviderName = 'plonebatch'
    batchSize = 10
    startBatchingAt = sys.maxint

    def renderRow(self, row, cssClass=None):
        if len(row):
            item, col, colspan = row[0]
            try:
                state = api.content.get_state(item)
            except WorkflowException:
                state = ''
            if state:
                cssClass = (' '.join([cssClass or '',
                                      'state-{0:s}'.format(state)])).strip()
        return super(PersonnelListing, self).renderRow(row, cssClass)

    def getBatchSize(self):
        return max(int(self.request.get(self.prefix + '-batchSize',
                                        self.batchSize)), 1)

    def setUpColumns(self):
        cols = super(PersonnelListing, self).setUpColumns()

        columns_display = getattr(self.context, 'columns_display', [])

        if columns_display:
            cols_factory = getUtility(IVocabularyFactory,
                                      name='collective.roster.displaycolumns')
            cols_vocabulary = cols_factory(self.context)
            cols_all = [col.value for col in cols_vocabulary]

            cols_selected = [col for col in cols
                             if col.__name__ in columns_display or
                             col.__name__ not in cols_all]
            return cols_selected

        # BBB: Roster used to support hiding explicitly hidden columns
        columns_hidden = getattr(self.context, 'columns_hidden', [])
        if columns_hidden:
            return filter(lambda x: x.__name__ not in columns_hidden, cols)

        return cols

    def orderColumns(self):
        columns_display = getattr(self.context, 'columns_display', [])
        if not columns_display:
            super(PersonnelListing, self).orderColumns()
        else:
            self.columnCounter = 0
            self.columns = sorted(
                self.columns, key=ColumnDisplaySortKey(columns_display))
            for col in self.columns:
                self.columnByName[col.__name__] = col
                idx = self.columnCounter
                col.id = '{0:s}-{1:s}-{2:d}'.format(
                    self.prefix, col.__name__, idx)
                self.columnIndexById[col.id] = idx
                self.columnCounter += 1

    @property
    @view.memoize
    def values(self):
        pc = api.portal.get_tool('portal_catalog')
        brains = pc(
            path='/'.join(self.context.getPhysicalPath()),
            object_provides=IPerson.__identifier__
        )
        values = map(lambda x: x.getObject(), brains)
        return values


class PersonnelAlphaListing(PersonnelListing):

    alpha = []
    sortOn = None

    @property
    def values(self):
        values = super(PersonnelAlphaListing, self).values
        sorted_values = sorted(values, key=sortable_title)
        return sorted_values

    def update(self):
        super(PersonnelAlphaListing, self).update()
        self.alpha = []


@adapter(IRoster, IBrowserRequest, PersonnelAlphaListing)
@implementer(IColumn)
class AlphaColumn(column.Column):
    weight = -1
    header = _(u'#')

    def renderCell(self, ob):
        if not ob.last_name:
            return u''
        alpha = ob.last_name[0].upper()

        if not self.table.alpha or alpha != self.table.alpha[-1]:
            self.table.alpha.append(alpha)
            return u'<a name="{0:s}">{1:s}</a>'.format(alpha, alpha)
        else:
            return u''


@adapter(IRoster, IBrowserRequest, IPersonnelListing)
@implementer(IColumn)
class DescriptionColumn(column.Column):
    weight = 98
    header = _(u'Description')

    def renderCell(self, ob):
        return ob.description


@adapter(IRoster, IBrowserRequest, IPersonnelListing)
@implementer(IColumn)
class NameColumn(column.LinkColumn):
    weight = 99
    header = _(u'Name')

    def getLinkURL(self, ob):
        return ob.absolute_url()

    def getLinkContent(self, ob):
        title = u'{0:s} {1:s}'.format(ob.last_name, ob.first_name)
        if type(title) != unicode:
            title = unicode(title, u'utf-8')
        return title


@adapter(IRoster, IBrowserRequest, IPersonnelListing)
@implementer(IColumn)
class PositionColumn(column.Column):
    weight = 100
    header = _(u'Title')

    def renderCell(self, ob):
        return ob.position

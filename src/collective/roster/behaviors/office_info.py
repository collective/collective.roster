# -*- coding: utf-8 -*-
from collective.roster import _
from collective.roster.behaviors.interfaces import IOfficeInfo
from collective.roster.behaviors.interfaces import ShortNumberWidget
from collective.roster.interfaces import IPersonnelListing
from collective.roster.interfaces import IRoster
from z3c.form.converter import IntegerDataConverter
from z3c.form.interfaces import IDataConverter
from z3c.table import column
from z3c.table.interfaces import IColumn
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IInt


@adapter(IRoster, IBrowserRequest, IPersonnelListing)
@implementer(IColumn)
class RoomColumn(column.Column):
    weight = 101
    header = _(u'Room')

    def renderCell(self, ob):
        adapted = IOfficeInfo(ob, None)
        if adapted:
            return getattr(adapted, 'room', None) or u''
        return u''


@adapter(IRoster, IBrowserRequest, IPersonnelListing)
@implementer(IColumn)
class ShortNumberColumn(column.LinkColumn):
    weight = 103
    header = _(u'Short number')

    def getLinkURL(self, ob):
        adapted = IOfficeInfo(ob, None)
        short_number = getattr(adapted, 'short_number', None)
        if short_number:
            return u'tel: {0:d}'.format(short_number)
        return u''

    def getLinkContent(self, ob):
        adapted = IOfficeInfo(ob, None)
        if adapted:
            return getattr(adapted, 'short_number', None) or u''
        return u''


@adapter(IInt, ShortNumberWidget)
@implementer(IDataConverter)
class ShortNumberDataConverter(IntegerDataConverter):
    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        return unicode(value)

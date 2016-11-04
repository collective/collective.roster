# -*- coding: utf-8 -*-
from collective.roster import _
from collective.roster.behaviors.interfaces import ISubjectInfo
from collective.roster.interfaces import IPersonnelListing
from collective.roster.interfaces import IRoster
from z3c.table import column
from z3c.table.interfaces import IColumn
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest


@adapter(IRoster, IBrowserRequest, IPersonnelListing)
@implementer(IColumn)
class SubjectColumn(column.LinkColumn):
    weight = 105
    header = _(u'Subject')

    def renderCell(self, obj):
        adapted = ISubjectInfo(obj, None)
        if adapted:
            return getattr(adapted, 'studysubject', None) or u''
        return u''

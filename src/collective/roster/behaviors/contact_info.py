# -*- coding: utf-8 -*-
from collective.roster import _
from collective.roster.behaviors.interfaces import IContactInfo
from collective.roster.interfaces import IPersonnelListing
from collective.roster.interfaces import IRoster
from z3c.table import column
from z3c.table.interfaces import IColumn
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest


@adapter(IRoster, IBrowserRequest, IPersonnelListing)
@implementer(IColumn)
class EmailColumn(column.LinkColumn):
    weight = 104
    header = _(u'Email')

    def getLinkURL(self, ob):
        adapted = IContactInfo(ob, None)
        email = getattr(adapted, 'email', None)
        if email:
            return u'mailto:{0:s}'.format(email)
        return u''

    def getLinkContent(self, ob):
        adapted = IContactInfo(ob, None)
        if adapted:
            return getattr(adapted, 'email', u'') or u''
        return u''


@adapter(IRoster, IBrowserRequest, IPersonnelListing)
@implementer(IColumn)
class PhoneNumberColumn(column.LinkColumn):
    weight = 102
    header = _(u'Phone number')

    def getLinkURL(self, ob):
        adapted = IContactInfo(ob, None)
        phone = getattr(adapted, 'phone_number', None)
        if phone:
            return u'tel:{0:s}'.format(phone)
        return u''

    def getLinkContent(self, ob):
        adapted = IContactInfo(ob, None)
        if adapted:
            return getattr(adapted, 'phone_number', u'') or u''
        return u''

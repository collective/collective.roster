# -*- coding: utf-8 -*-

from five import grok

from collective.roster.person import PersonViewlets

from collective.roster.behaviors.interfaces import (
    IContactInfo,
    IOfficeInfo
)


class ContactInfoViewlet(grok.Viewlet):
    """Viewlet for rendering the contact info."""
    grok.viewletmanager(PersonViewlets)
    grok.context(IContactInfo)
    grok.name("collective.roster.personviewlets.contactinfo")


class OfficeInfoViewlet(grok.Viewlet):
    """Viewlet for rendering the office info."""
    grok.viewletmanager(PersonViewlets)
    grok.context(IOfficeInfo)
    grok.name("collective.roster.personviewlets.officeinfo")

from five import grok
from collective.roster.person import PersonViewlets

from collective.roster.behaviors.interfaces import (
    IHasContactInfo,
    IHasRelatedPersons,
    IContactInfo
)

from Products.CMFCore.utils import getToolByName
from plone.uuid.interfaces import IUUID


class ContactInfoViewlet(grok.Viewlet):
    """Renders the contact info"""

    grok.viewletmanager(PersonViewlets)
    grok.context(IHasContactInfo)
    grok.name("collective.roster.personviewlets.contactinfo")

    @property
    def email(self):
        return IContactInfo(self.context).email

    @property
    def phone_number(self):
        return IContactInfo(self.context).phone_number


class RelatedPersonViewlet(grok.Viewlet):
    """Renders person related items"""

    grok.viewletmanager(PersonViewlets)
    grok.context(IHasRelatedPersons)
    grok.name("collective.roster.personviewlets.relatedperson")

    @property
    def related_items(self):
        pc = getToolByName(self.context, "portal_catalog")
        result = pc(related_persons=[IUUID(self.context)])
        # Here is the problem, can't find any indexes?



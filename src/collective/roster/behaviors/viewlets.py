from five import grok
from collective.roster.person import PersonViewlets
from collective.roster.behaviors.interfaces import IHasContactInfo
from collective.roster.behaviors.interfaces import IContactInfo


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
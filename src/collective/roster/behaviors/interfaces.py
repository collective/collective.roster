from plone.directives import form
from zope import schema
from collective.roster import _
from zope.interface import alsoProvides
from plone.formwidget.contenttree import UUIDSourceBinder
from plone.formwidget.contenttree.widget import MultiContentTreeFieldWidget

from zope.interface import Interface
from zope.schema import ValidationError

class InvalidEmailAddress(ValidationError):
    "Invalid email address"

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

class IContactInfo(form.Schema):
    """ Behavior interface for providing contact info """

 # Feedback fieldset
    
    form.fieldset(
        'Contact Information', 
        label=_(u"Contact Information"),
        fields=['email', 'phone_number']
    )
    

    email = schema.TextLine(
        title=_(u"Email"),
        description=_(u"Email address"),
        constraint=validateaddress
    )

    phone_number = schema.TextLine(
        title=_(u"Phone"),
        description=_(u"Phone number"),
    )
alsoProvides(IContactInfo, form.IFormFieldProvider)


class IHasContactInfo(Interface):
    """ Marker interface for contact info behavior """


class IHasRelatedPersons(Interface):
    """Marker interface for related persons behavior"""
    
class IRelatedPersons(form.Schema):
    """Behavior interface which provides related persons for
    any dexterity content"""
    form.widget(related_persons=MultiContentTreeFieldWidget)
    related_persons = schema.List(
        title=u"Related persons",
        description=u"Search for person that is related to this item",
        value_type=schema.Choice(
            source=UUIDSourceBinder(portal_type="collective.roster.person")
        )
    )
alsoProvides(IRelatedPersons, form.IFormFieldProvider)

# -*- coding: utf-8 -*-

from plone.directives import form

from zope import schema
from zope.schema import ValidationError

from zope.interface import (
    Interface,
    alsoProvides
)

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from plone.formwidget.contenttree import UUIDSourceBinder
from plone.formwidget.contenttree.widget import MultiContentTreeFieldWidget

from collective.roster import _


class InvalidEmailAddress(ValidationError):
    """Invalid email address.
    """


def isEmailAddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


class IOfficeInfo(form.Schema):
    """Behavior interface for providing office info.
    """

    room = schema.TextLine(
        title=_(u"Room"),
        description=_(u"Room Info"),
    )

    form.fieldset(
        'Contact information',
        label=_(u"Office information"),
        fields=['room']
    )
alsoProvides(IOfficeInfo, form.IFormFieldProvider)


class IContactInfo(form.Schema):
    """Behavior interface for providing contact info.
    """

    email = schema.TextLine(
        title=_(u"Email"),
        constraint=isEmailAddress,
        required=False
    )

    phone_number = schema.TextLine(
        title=_(u"Phone"),
        required=False
    )

    short_number = schema.TextLine(
        title=_(u"Short number"),
        required=False
    )

    form.fieldset(
        'Contact information',
        label=_(u"Contact information"),
        fields=['email', 'phone_number', 'short_number']
    )

alsoProvides(IContactInfo, form.IFormFieldProvider)


class IAutoRoles(Interface):
    """Marker interface for auto-roles behavior.
    """


class IRelatedPersons(form.Schema):
    """Behavior interface which provides related persons for any dexterity
    content. Related persons behavior is to link content to persons.

    """
    form.widget(related_persons=MultiContentTreeFieldWidget)
    related_persons = schema.List(
        title=u"Related persons",
        description=u"Search for person that is related to this item",
        value_type=schema.Choice(
            source=UUIDSourceBinder(portal_type="collective.roster.person")
        )
    )

alsoProvides(IRelatedPersons, form.IFormFieldProvider)


class IHasRelatedPersons(Interface):
    """Marker interface for related persons behavior.
    """

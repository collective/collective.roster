# -*- coding: utf-8 -*-
from collective.roster import _
from collective.roster.interfaces import discriminators
from plone.autoform.directives import order_after
from plone.autoform.directives import order_before
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.formwidget.contenttree import UUIDSourceBinder
from plone.formwidget.contenttree.widget import MultiContentTreeFieldWidget
from plone.i18n.normalizer import IIDNormalizer
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.text import TextWidget
from z3c.form.validator import SimpleFieldValidator
from z3c.form.widget import FieldWidget
from zope import schema
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.interface import Invalid
from zope.schema import ValidationError


try:
    from Products.CMFPlone.RegistrationTool import checkEmailAddress
except ImportError:
    from Products.CMFDefault.utils import checkEmailAddress

try:
    from Products.CMFPlone.RegistrationTool import EmailAddressInvalid
except ImportError:
    from Products.CMFDefault.exceptions import EmailAddressInvalid


class InvalidEmailAddress(ValidationError):
    """Invalid email address
    """


def is_email_address(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


class InvalidShortNumber(ValidationError):
    """Invalid short number
    """


def is_short_number(value):
    if value < 99 or value > 9999:
        raise InvalidShortNumber(value)
    return True


class IContactInfo(model.Schema):
    """Behavior schema
    """
    email = schema.TextLine(
        title=_(u'Email'),
        constraint=is_email_address,
        required=False
    )
    phone_number = schema.TextLine(
        title=_(u'Phone'),
        required=False,
    )
    fieldset(
        'Contact information',
        label=_(u'Contact information'),
        fields=['email', 'phone_number']
    )
alsoProvides(IContactInfo, IFormFieldProvider)


class ISubjectInfo(model.Schema):
    """Behavior schema
    """
    studysubject = schema.TextLine(
        title=_(u'Subject'),
        required=False
    )
    fieldset(
        'Contact information',
        label=_(u'Contact information'),
        fields=['studysubject']
    )
alsoProvides(ISubjectInfo, IFormFieldProvider)


class ShortNumberWidget(TextWidget):
    """Widget for displaying short numbers properly
    """


def ShortNumberFieldWidget(field, request):
    return FieldWidget(field, ShortNumberWidget(request))


class IOfficeInfo(model.Schema):
    """Behavior schema
    """
    order_after(room='IContactInfo.phone_number')
    room = schema.TextLine(
        title=_(u'Room'),
        # description=_(u'Room Info'),
        required=False
    )

    order_after(short_number='IContactInfo.phone_number')
    widget(short_number=ShortNumberFieldWidget)
    short_number = schema.Int(
        title=_(u'Short number'),
        required=False,
        constraint=is_short_number
    )
alsoProvides(IOfficeInfo, IFormFieldProvider)


class IRelatedPersons(model.Schema):
    """Behavior schema
    """
    widget(related_persons=MultiContentTreeFieldWidget)
    related_persons = schema.List(
        title=u'Related persons',
        description=u'Search for persons related to this item',
        value_type=schema.Choice(
            source=UUIDSourceBinder(portal_type='collective.roster.person')
        )
    )
alsoProvides(IRelatedPersons, IFormFieldProvider)


class IHasRelatedPersons(Interface):
    """Marker interface
    """


class IGroupsProvider(Interface):
    """Behavior schema
    """
    order_before(groups='columns_display')
    groups = schema.List(
        title=_(u'Groups'),
        description=_('roster_groups_help',
                      default=u'group_id|Group title'),
        value_type=schema.TextLine(
            title=_(u'Group'),
            required=True
        ),
        required=False
    )
alsoProvides(IGroupsProvider, IFormFieldProvider)


@discriminators(field=IGroupsProvider['groups'])
class GroupNameValidator(SimpleFieldValidator):
    def validate(self, value, force=False):
        value = value or []
        super(SimpleFieldValidator, self).validate(value, force)

        normalizer = getUtility(IIDNormalizer)
        normalized = map(normalizer.normalize, value)

        if len(set(normalized)) != len(value):
            raise Invalid(_(u'Roster display groups must be unique.'))


class IProvidesGroups(Interface):
    """Marker interface
    """


class IGroups(model.Schema):
    """Behavior schema
    """
    widget(groups=CheckBoxFieldWidget)
    groups = schema.List(
        title=_(u'Groups'),
        value_type=schema.Choice(
            title=_(u'Group'),
            vocabulary='collective.roster.localgroups'
        ),
        missing_value=[],
        required=False
    )
alsoProvides(IGroups, IFormFieldProvider)


class IHasGroups(Interface):
    """Marker interface
    """


class IGroupsAsSubjects(model.Schema):
    """Marker interface
    """


class IAutoRoles(Interface):
    """Marker interface
    """

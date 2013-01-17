""" Personnel roster and person related interfaces and schemas """

from zope import schema

from zope.interface import (
    alsoProvides,
    Interface
)

from plone.directives import form

from z3c.form.browser.checkbox import CheckBoxFieldWidget

from collective.roster import _
from plone.namedfile.field import NamedBlobImage


class IPersonnelListing(Interface):
    """ Marker interface for personnel listing tables """


class IHiddenColumnsField(Interface):
    """ Marker interface for roster hidden columns field """


class IRoster(form.Schema):
    """ Personnel roster (to contain and display persons). Contained persons
    can be assigned into one ore more groups. """

    groups = schema.List(
        title=_(u"Groups"),
        value_type=schema.TextLine(
            title=_(u"Group"),
            required=True
        ),
        min_length=1,
        required=True
    )

    columns_hidden = schema.List(
        # README: We must do this backwards to auto-enable the new columns
        # we may introduce with upgdates or add-ons. That is, the user does
        # a white list of displayed columns, but what is actually stored is
        # a black list of hidden columns.
        title=_(u"Display columns"),
        description=_(u"Display only the selected person information columns "
                      u"on supporting views."),
        value_type=schema.Choice(
            title=_("Column"),
            vocabulary="collective.roster.columns",
        ),
    )

alsoProvides(IRoster['columns_hidden'], IHiddenColumnsField)
# ^ Enables our custom data manager for the hidden columns field.


class IPerson(form.Schema):
    """ A person to store and display person related information """

    title = schema.TextLine(
        title=_(u"Title"),
        readonly=True, required=False,
    )

    firstname = schema.TextLine(
        title=_(u"First name")
    )

    lastname = schema.TextLine(
        title=_(u"Last name")
    )

    salutation = schema.TextLine(
        title=_(u"Preferred salutation"),
        missing_value=u"",
        required=False
    )

    description = schema.Text(
        title=_(u"Description"),
        missing_value=u"",
        required=False
    )

    biography = schema.Text(
        title=_(u"Biography"),
        missing_value=u"",
        required=False
    )
    
    form.primary('image')
    image = NamedBlobImage(
        title=_(u"Upload an image"),
        required=False,
    ) 

    form.widget(groups=CheckBoxFieldWidget)
    groups = schema.List(
        title=_(u"Groups"),
        value_type=schema.Choice(
            title=_("Group"),
            vocabulary="collective.roster.localgroups"
        ),
        # min_length=1,
        required=False
    )

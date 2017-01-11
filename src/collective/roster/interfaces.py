""" Personnel roster and person related interfaces and schemas """
from plone.i18n.normalizer.interfaces import IIDNormalizer


from zope import schema

from zope.interface import (
    alsoProvides,
    Interface,
    Invalid
)
from zope.component import getUtility

from plone.directives import form

from z3c.form.browser.checkbox import CheckBoxFieldWidget

from collective.roster import _
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText

from collective.roster.utils import validate_image_file_extension


class IPersonnelListing(Interface):
    """ Marker interface for personnel listing tables """


#class IHiddenColumnsField(Interface):
#    """ Marker interface for roster hidden columns field """


class IPersonTitle(Interface):
    """ Implement to customize person title formatting """


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

#    columns_hidden = schema.List(
#        # README: We must do this backwards to auto-enable the new columns
#        # we may introduce with upgdates or add-ons. That is, the user does
#        # a white list of displayed columns, but what is actually stored is
#        # a black list of hidden columns.
#        title=_(u"Display columns"),
#        description=_(u"Display only the selected person information columns "
#                      u"on supporting views."),
#        value_type=schema.Choice(
#            title=_("Column"),
#            vocabulary="collective.roster.columns",
#        ),
#    )

    columns_display = schema.List(

        title=_(u"Display columns"),
        description=_(u"Display only the selected person information columns "
                      u"on supporting views."),
        value_type=schema.Choice(
            title=_("Column"),
            vocabulary="collective.roster.columns",
        ),
    )


#alsoProvides(IRoster['columns_hidden'], IHiddenColumnsField)
# ^ Enables our custom data manager for the hidden columns field.
class IPerson(form.Schema):
    """ A person to store and display person related information """

    title = schema.TextLine(
        title=_(u"Title"),
        readonly=True, required=False,
    )

    first_name = schema.TextLine(
        title=_(u"First name")
    )

    last_name = schema.TextLine(
        title=_(u"Last name")
    )

    salutation = schema.TextLine(  # !sic
        title=_(u"Title"),
        description=_("example: 'doctor' or 'designer'"),
        missing_value=u"",
        required=False
    )

    description = schema.Text(
        title=_(u"Description"),
        missing_value=u"",
        required=False
    )

    form.primary('biography')
    biography = RichText(
        title=_(u"Biography"),
        required=False
    )

    form.primary('image')
    image = NamedBlobImage(
        title=_(u"Upload an image"),
        required=False,
        constraint=validate_image_file_extension
    )

    form.widget(groups=CheckBoxFieldWidget)
    groups = schema.List(
        title=_(u"Groups"),
        value_type=schema.Choice(
            title=_("Group"),
            vocabulary="collective.roster.localgroups"
        ),
        # min_length=1,
        missing_value=[],
        required=False
    )


@form.validator(field=IRoster['groups'])
def validateGroupsList(value):

    normalizer = getUtility(IIDNormalizer)
    normalized = map(normalizer.normalize, value)

    if len(set(normalized)) != len(value):
        raise Invalid(_(u"Duplicates in Groups"))

@form.validator(field=IPerson['first_name'])
@form.validator(field=IPerson['last_name'])
def validateName(value):

    normalizer = getUtility(IIDNormalizer)
    if not len(normalizer.normalize(value)):
        raise Invalid(_(u"No valid characters"))

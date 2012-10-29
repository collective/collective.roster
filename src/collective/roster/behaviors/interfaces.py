from plone.directives import form
from zope import schema
from collective.roster import _
from zope.interface import alsoProvides


class IContactInfo(form.Schema):
    """ Interface for providing contact info """

    email = schema.TextLine(
        title=_(u"Email"),
        description=_(u"Email address"),
    )

    phone_number = schema.TextLine(
        title=_(u"Phone"),
        description=_(u"Phone number"),
    )

alsoProvides(IContactInfo, form.IFormFieldProvider)

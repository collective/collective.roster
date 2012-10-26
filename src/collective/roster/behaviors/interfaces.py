from plone.directives import form
from zope import schema
from collective.roster import _
from zope.interface import alsoProvides


class IContactInfo(form.Schema):
    """ Interface for providing contact info """

    email = schema.TextLine(
        title=_(u"From"),
        description=_(u"Form letter sender"),
    )

alsoProvides(IContactInfo, form.IFormFieldProvider)

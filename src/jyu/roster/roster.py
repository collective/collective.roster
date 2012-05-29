from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.textfield import RichText

class IRoster(form.Schema):
    """The personnel roster.
    """

    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Roster title"),
        )

    description = schema.Text(
            title=_(u"Session summary"),
        )

    details = RichText(
            title=_(u"Session details"),
            required=False
        )

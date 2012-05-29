from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from jyu.roster import _

class IPerson(form.Schema):
    """A person in the roster. It can be any role.
    """

    title = schema.TextLine(
            title=_(u"Name"),
        )

    description = schema.Text(
            title=_(u"A short summary"),
        )

    bio = RichText(
            title=_(u"Bio"),
            required=False
        )

    picture = NamedImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
        )

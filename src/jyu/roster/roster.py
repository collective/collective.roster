from five import grok
from zope import schema

from zope.interface import Invalid

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from jyu.roster.interfaces import MessageFactory as _

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

#    rosterPersonnel = RelationList(
#        title=_(u"Highlighted films"),
#        description=_(u"Personnel to connect to the roster"),
#        value_type=RelationChoice(
#               source=ObjPathSourceBinder(
#                   object_provides=IPerson.__identifier__
#                ),
#             ),
#           required=False,
#    )


class View(grok.View):
    #dexterity.DisplayForm in manual's code, instead of grok.View
    """Default view (called "@@view"") for a cinema.
    
    The associated template is found in cinema_templates/view.pt.
    """

    grok.context(IRoster)
    grok.require('zope2.View')
    grok.name('view')


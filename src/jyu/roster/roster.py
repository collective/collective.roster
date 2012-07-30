from five import grok
from zope import schema

from zope.interface import Invalid

from plone.directives import form, dexterity
from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from jyu.roster.person import IPerson, IPortalRoles

from jyu.roster.interfaces import MessageFactory as _

class IRoster(form.Schema):
    """The personnel roster.
    """

    title = schema.TextLine(
            title=_(u"Title"),
            description=_(u"Roster title"),
        )

    description = schema.Text(
            title=_(u"Roster description"),
        )

class View(grok.View):
    
    grok.context(IRoster)
    grok.require('zope2.View')
    grok.name('view')

    def people(self):
        """Return a catalog search result of people to show
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(object_provides=IPerson.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='sortable_title')

    def subjects(self):
        """Return a catalog search result of subjects to show
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(object_provides=IPortalRoles.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='sortable_title')


from plone.app.viewletmanager.manager import OrderedViewletManager


class RosterViewletManager(OrderedViewletManager, grok.ViewletManager):
    grok.context(IRoster)
    grok.name("jyu.roster.roster")


class RosterViewlet(grok.Viewlet):
   grok.context(IRoster)
   grok.viewletmanager(RosterViewletManager)
   grok.name("jyu.roster.roster.details")




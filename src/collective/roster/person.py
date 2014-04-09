# -*- coding: utf-8 -*-
"""Person.
"""

from five import grok
from plone.directives import dexterity

from zope.lifecycleevent.interfaces import (
    IObjectModifiedEvent,
    IObjectCreatedEvent
)

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from plone.indexer import indexer
from plone.uuid.interfaces import IUUID

from plone.app.viewletmanager.manager import (
    OrderedViewletManager,
    ManageViewlets
)

from plone.app.content.interfaces import INameFromTitle

from collective.roster.interfaces import IPerson, IPersonTitle


class NameFromTitle(grok.Adapter):
    grok.provides(INameFromTitle)
    grok.context(IPerson)

    @property
    def title(self):
        return u"%s %s" % (self.context.last_name,
                           self.context.first_name)


def personTitle(context):
    """Generates formatted titles for persons."""

    title = INameFromTitle(context).title
    adapted = IPerson(context, None)
    if adapted:
        bound = IPerson["salutation"].bind(adapted)
        salutation = bound.get(adapted)
        if salutation:
            title = u"%s, %s" % (title, salutation)
    return title


@grok.subscribe(IPerson, IObjectCreatedEvent)
@grok.subscribe(IPerson, IObjectModifiedEvent)
def updatePersonTitle(context, event):
    context.title = IPersonTitle(context, None) or personTitle(context)
    context.reindexObject(idxs=('Title',))


@indexer(IPerson)
def title(context):
    title = IPersonTitle(context, None) or personTitle(context)
    if isinstance(title, unicode):
        title = title.encode("utf-8", "ignore")
    return title
grok.global_adapter(title, name="Title")


class View(dexterity.DisplayForm):
    """ Person main view, which mainly renders the person viewlet manager """

    grok.context(IPerson)
    grok.require("zope2.View")
    grok.name("view")

    #@property
    #def room(self):
        #adapter = IOfficeInfo(obj, None)
        #if adapter:
            #return getattr(adapter, "room", None) or u""
        #return u""


class PersonViewlets(OrderedViewletManager, grok.ViewletManager):
    """ Person viewlet manager, which manages all person related viewlets """
    grok.context(IPerson)
    grok.name("collective.roster.personviewlets")


class ManagePersonViewlets(View, ManageViewlets):
    grok.context(IPerson)
    grok.name("manage-viewlets")

    def index(self):
        # ManageViewlets.__call__ may call this at its end, and then we'd like
        # to render by using our dexterity.DisplayForm based View-class.
        return View.__call__(self)

    def __call__(self):
        return ManageViewlets.__call__(self)


class GroupsViewlet(grok.Viewlet):
    """ Groups viewlet, which render list of groups the person belongs to """

    grok.viewletmanager(PersonViewlets)
    grok.context(IPerson)
    grok.name("collective.roster.personviewlets.localgroups")

    @property
    def groups(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name="collective.roster.localgroups")
        vocabulary = vocabulary_factory(self.context)

        terms = filter(lambda term: term.value in self.context.groups,
                       vocabulary)
        titles = map(lambda term: term.title, terms)
        return titles


class PortraitViewlet(grok.Viewlet):
    """ Portrait viewlet, which renders the portrait image """

    grok.viewletmanager(PersonViewlets)
    grok.context(IPerson)
    grok.name("collective.roster.personviewlets.portrait")


class PersonViewlet(grok.Viewlet):
    """ Person viewlet, which renders the person image """

    grok.viewletmanager(PersonViewlets)
    grok.context(IPerson)
    grok.name("collective.roster.personviewlets.person")


class RelatedContentViewlet(grok.Viewlet):
    """ Related content viewlet, which renders list of content linked to the
    person """

    grok.viewletmanager(PersonViewlets)
    grok.context(IPerson)
    grok.name("collective.roster.personviewlets.relatedcontent")

    @property
    def related_items(self):
        pc = getToolByName(self.context, "portal_catalog")
        results = pc(related_persons=[IUUID(self.context)])
        return results

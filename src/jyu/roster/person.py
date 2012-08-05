# -*- coding: utf-8 -*-
"""Person"""

from five import grok

from plone.indexer import indexer
from plone.app.viewletmanager.manager import OrderedViewletManager

from plone.app.content.interfaces import INameFromTitle

from jyu.roster.schemas import IPerson

from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
_ = ZopeMessageFactory("jyu.roster")


class NameFromTitle(grok.Adapter):
    grok.provides(INameFromTitle)
    grok.context(IPerson)

    @property
    def title(self):
        return u"%s %s" % (self.context.firstname,
                           self.context.lastname)


@indexer(IPerson)
def title(obj):
    if obj.salutation:
        obj.title = u"%s %s" % (obj.salutation, INameFromTitle(obj).title)
    else:
        obj.title = INameFromTitle(obj).title
    return obj.title.encode('utf-8')  # XXX: Unicode would crash the indexing.
grok.global_adapter(title, name="Title")


class View(grok.View):
    """"Person view"""

    grok.context(IPerson)
    grok.require("zope2.View")
    grok.name("view")


class PersonViewlets(OrderedViewletManager, grok.ViewletManager):
    grok.context(IPerson)
    grok.name("jyu.roster.personviewlets")


class ExampleViewlet(grok.Viewlet):
    """Example viewlet"""

    grok.viewletmanager(PersonViewlets)
    grok.context(IPerson)
    grok.name("jyu.roster.personviewlets.example")


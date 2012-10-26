# -*- coding: utf-8 -*-
"""Person"""

from five import grok

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from plone.indexer import indexer
from plone.app.viewletmanager.manager import OrderedViewletManager

from plone.app.content.interfaces import INameFromTitle

from collective.roster.schemas import IPerson

from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
_ = ZopeMessageFactory("collective.roster")


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


@indexer(IPerson)
def subject(obj):
    vocabulary_factory = getUtility(IVocabularyFactory,
                                    name="collective.roster.localgroups")
    vocabulary = vocabulary_factory(obj)

    terms = filter(lambda term: term.value in obj.groups, vocabulary)
    groups = map(lambda term: term.value, terms)

    return obj.subject + tuple(groups)
grok.global_adapter(subject, name="Subject")


class View(grok.View):
    """"Person view"""

    grok.context(IPerson)
    grok.require("zope2.View")
    grok.name("view")


class PersonViewlets(OrderedViewletManager, grok.ViewletManager):
    grok.context(IPerson)
    grok.name("collective.roster.personviewlets")


class GroupsViewlet(grok.Viewlet):
    """Groups viewlet"""

    grok.viewletmanager(PersonViewlets)
    grok.context(IPerson)
    grok.name("collective.roster.personviewlets.localgroups")

    def render(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name="collective.roster.localgroups")
        vocabulary = vocabulary_factory(self.context)

        terms = filter(lambda term: term.value in self.context.groups,
                       vocabulary)
        titles = map(lambda term: term.title, terms)

        return u"<p>%s</p>" % ", ".join(titles)


class ExampleViewlet(grok.Viewlet):
    """Example viewlet"""

    grok.viewletmanager(PersonViewlets)
    grok.context(IPerson)
    grok.name("collective.roster.personviewlets.example")

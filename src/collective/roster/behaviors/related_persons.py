# -*- coding: utf-8 -*-
from collective.roster.behaviors.interfaces import IHasRelatedPersons
from collective.roster.behaviors.interfaces import IRelatedPersons
from plone import api
from plone.indexer import indexer
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.viewlet.viewlet import ViewletBase
from zope.interface import Interface

import os


# noinspection PyUnusedLocal
@indexer(Interface)
def skipIndex(ob):
    raise AttributeError


@indexer(IHasRelatedPersons)
def indexRelatedPersons(ob):
    adapted = IRelatedPersons(ob)
    bound = IRelatedPersons['related_persons'].bind(adapted)
    return bound.get(adapted)


class RelatedContentViewlet(ViewletBase):
    index = ViewPageTemplateFile(os.path.join('templates',
                                              'related_content_viewlet.pt'))

    @property
    def related_items(self):
        pc = api.portal.get_tool('portal_catalog')
        results = pc(related_persons=[IUUID(self.context)])
        return results

    def render(self):
        return self.index()

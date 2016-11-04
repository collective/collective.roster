# -*- coding: utf-8 -*-
from plone.app.viewletmanager.manager import ManageViewlets
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.viewlet.viewlet import ViewletBase
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import os


class ManagePersonViewlets(DefaultView, ManageViewlets):

    def index(self):
        # ManageViewlets.__call__ may call this at its end, and then we'd like
        # to render by using our dexterity.DisplayForm based View-class.
        # noinspection PyCallByClass
        return DefaultView.__call__(self)

    def __call__(self):
        self.update()
        return ManageViewlets.__call__(self)


class GroupsViewlet(ViewletBase):
    index = ViewPageTemplateFile(os.path.join('templates',
                                              'person_groups_viewlet.pt'))

    @property
    def groups(self):
        vocabulary_factory = getUtility(IVocabularyFactory,
                                        name='collective.roster.localgroups')
        vocabulary = vocabulary_factory(self.context)

        terms = filter(lambda term: term.value in (self.context.groups or []),
                       vocabulary)
        titles = map(lambda term: term.title, terms)
        return titles

    def render(self):
        return self.index()

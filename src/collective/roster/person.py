# -*- coding: utf-8 -*-
"""A person to store and display person related information
"""
from collective.roster import _
from collective.roster.interfaces import IPerson
from collective.roster.interfaces import IPersonTitle
from plone import api
from plone.app.content.interfaces import INameFromTitle
from zope.component import adapter
from zope.component.interfaces import IObjectEvent
from zope.i18n import translate
from zope.interface import implementer


@adapter(IPerson)
@implementer(INameFromTitle)
class PersonNameFromTitle(object):
    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        title = _('person_name',
                  default=u'${last_name} ${first_name}',
                  mapping={'first_name': IPerson(self.context).first_name,
                           'last_name': IPerson(self.context).last_name})
        return translate(title, context=api.portal.getRequest())


# Note: This is left unregistered by purpose to make overriding easier
@implementer(IPersonTitle)
def person_title(person):
    title = INameFromTitle(person).title
    adapted = IPerson(person, None)
    if adapted:
        bound = IPerson['position'].bind(adapted)
        position = bound.get(adapted)
        title_position = _('person_title',
                           default=u'${title}, ${position}',
                           mapping={'title': title,
                                    'position': position})
        if position:
            title = translate(title_position, context=api.portal.getRequest())
    return title


# noinspection PyUnusedLocal
@adapter(IPerson, IObjectEvent)
def update_person_title(person, event=None):
    person.title = IPersonTitle(person, None) or person_title(person)
    person.reindexObject(idxs=('Title',))

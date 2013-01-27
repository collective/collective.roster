# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName


def upgrade4to5(context):
    import pdb; pdb.set_trace()

    from collective.roster.interfaces import IPerson

    import plone.dexterity
    import plone.folder

    pc = getToolByName(context, "portal_catalog")

    all_brains = pc.unrestrictedSearchResults({
        'object_provides': [IPerson.__identifier__]
    })

    for brain in all_brains:
        obj = brain._unrestrictedGetObject()
        if obj.__class__ == plone.dexterity.content.Item:
            obj.__class__ = plone.dexterity.content.Container
            description = getattr(obj, "description", u"")
            plone.folder.ordered.CMFOrderedBTreeFolderBase.__init__(
                obj, obj.id, obj.title)
            if description:
                setattr(obj, "description", description)
            obj._p_changed = True

    for brain in all_brains:
        obj = brain._unrestrictedGetObject()

        firstname = getattr(obj, "firstname", u"")
        if firstname:
            obj.first_name = firstname
            del obj.__dict__["firstname"]

        lastname = getattr(obj, "lastname", u"")
        if lastname:
            obj.last_name = lastname
            del obj.__dict__["lastname"]

    return u"Upgraded collectige.roster from 4 to 5."

# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName


def upgrade4to5(context):

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

    return u"Upgraded collective.roster from 4 to 5."


def upgrade5to6(context):

    from collective.roster.interfaces import IPerson
    from collective.roster.behaviors.interfaces import IContactInfo

    pc = getToolByName(context, "portal_catalog")

    all_brains = pc.unrestrictedSearchResults({
        'object_provides': [IPerson.__identifier__]
    })

    from plone.behavior.annotation import AnnotationsFactoryImpl
    from zope.annotation.interfaces import IAnnotations

    for brain in all_brains:
        obj = brain._unrestrictedGetObject()
        annotations = IAnnotations(obj)
        prefix = AnnotationsFactoryImpl(obj, IContactInfo).prefix
        adapted = IContactInfo(obj, None)

        if adapted:

            email_key = "%semail" % prefix
            if email_key in annotations:
                email = annotations[email_key]
                del annotations[email_key]
                bound = IContactInfo["email"].bind(adapted)
                bound.set(adapted, email)

            phone_number_key = "%sphone_number" % prefix
            if phone_number_key in annotations:
                phone_number = annotations[phone_number_key]
                del annotations[phone_number_key]
                bound = IContactInfo["phone_number"].bind(adapted)
                bound.set(adapted, phone_number)

    return u"Upgraded collective.roster from 5 to 6."

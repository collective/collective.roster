# -*- coding: utf-8 -*-

# noinspection PyProtectedMember
from plone import api


def upgrade4to5(context):
    """Fix classes to be containers; Fix membrane compatibility
    """
    from collective.roster.interfaces import IPerson

    import plone.dexterity
    import plone.folder

    pc = api.portal.get_tool('portal_catalog')

    all_brains = pc.unrestrictedSearchResults({
        'object_provides': [IPerson.__identifier__]
    })

    for brain in all_brains:
        obj = brain._unrestrictedGetObject()
        if obj.__class__ == plone.dexterity.content.Item:
            obj.__class__ = plone.dexterity.content.Container
            description = getattr(obj, 'description', u'')
            plone.folder.ordered.CMFOrderedBTreeFolderBase.__init__(
                obj, obj.id, obj.title)
            if description:
                setattr(obj, 'description', description)
            obj._p_changed = True

    for brain in all_brains:
        obj = brain._unrestrictedGetObject()

        firstname = getattr(obj, 'firstname', u'')
        if firstname:
            obj.first_name = firstname
            del obj.__dict__['firstname']

        lastname = getattr(obj, 'lastname', u'')
        if lastname:
            obj.last_name = lastname
            del obj.__dict__['lastname']

    return u'Upgraded profile-collective.roster:default from version 4 to 5.'


# noinspection PyProtectedMember
def upgrade5to6(context):
    """Fix membrane compatibility by moving fields into attributes
    """
    from collective.roster.interfaces import IPerson
    from collective.roster.behaviors.interfaces import IContactInfo

    pc = api.portal.get_tool('portal_catalog')
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
            email_key = '{0:s}email'.format(prefix)
            if email_key in annotations:
                email = annotations[email_key]
                del annotations[email_key]
                bound = IContactInfo['email'].bind(adapted)
                bound.set(adapted, email)

            phone_number_key = '{0:s}phone_number'.format(prefix)
            if phone_number_key in annotations:
                phone_number = annotations[phone_number_key]
                del annotations[phone_number_key]
                bound = IContactInfo['phone_number'].bind(adapted)
                bound.set(adapted, phone_number)

    return u'Upgraded profile-collective.roster:default from version 5 to 6.'


# noinspection PyProtectedMember
def upgrade14to15(context):
    """Fix change in schema attribute name
    """
    from collective.roster.interfaces import IPerson
    from collective.roster.interfaces import IRoster

    pc = api.portal.get_tool('portal_catalog')
    results = pc.unrestrictedSearchResults({
        'object_provides': [IPerson.__identifier__]
    })
    for brain in results:
        ob = brain._unrestrictedGetObject()
        ob.position = getattr(ob, 'salutation', u'')
        delattr(ob, 'salutation')

    results = pc.unrestrictedSearchResults({
        'object_provides': [IRoster.__identifier__]
    })
    for brain in results:
        # noinspection PyProtectedMember
        ob = brain._unrestrictedGetObject()
        columns_display = []
        for column in ob.columns_display:
            if column == 'collective.roster.personnellisting.salutation':
                columns_display.append(
                    'collective.roster.personnellisting.position')
            else:
                columns_display.append(column)
        ob.columns_display = columns_display
        try:
            columns_hidden = []
            for column in ob.columns_hidden:
                if column == 'collective.roster.personnellisting.salutation':
                    columns_hidden.append(
                        'collective.roster.personnellisting.position')
                else:
                    columns_hidden.append(column)
            ob.columns_hidden = columns_display
        except AttributeError:
            pass

        types_tool = api.portal.get_tool('portal_types')
        types_tool['collective.roster.roster'].default_view = 'groups_view'

    return u'Upgraded profile-collective.roster:default from version 14 to 15.'

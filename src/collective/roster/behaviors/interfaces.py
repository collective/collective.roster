from plone.directives import form
from zope import schema
from collective.roster import _
from zope.interface import alsoProvides
from plone.formwidget.contenttree import UUIDSourceBinder
from plone.formwidget.contenttree.widget import MultiContentTreeFieldWidget


class IContactInfo(form.Schema):
    """ Behavior interface for providing contact info """

    email = schema.TextLine(
        title=_(u"Email"),
        description=_(u"Email address"),
    )

    phone_number = schema.TextLine(
        title=_(u"Phone"),
        description=_(u"Phone number"),
    )
alsoProvides(IContactInfo, form.IFormFieldProvider)


class IRelatedPersons(form.Schema):
    """Behavior interface which provides related persons for any dexterity content """
    form.widget(related_persons=MultiContentTreeFieldWidget)
    related_persons = schema.List(
        title=u"Related persons",
        description=u"Search for person that is related to this item",
        value_type=schema.Choice(
            source=UUIDSourceBinder(portal_type="collective.roster.person")
        )
    )
alsoProvides(IRelatedPersons, form.IFormFieldProvider)


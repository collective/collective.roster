# -*- coding: utf-8 -*-
from zope.interface import Interface
from plone.directives import form
from zope import schema
from collective.roster import _
from z3c.form.browser.checkbox import CheckBoxFieldWidget


class IPersonnelListing(Interface):
    """Marker interface for personnel listing tables"""


class IRoster(form.Schema):
    """Personnel roster"""

    groups = schema.List(
        title=_(u"Groups"),
        value_type=schema.TextLine(
            title=_(u"Group"),
            required=True
        ),
        min_length=1,
        required=True
    )


class IPerson(form.Schema):
    """A person"""

    title = schema.TextLine(
        title=_(u"Title"),
        readonly=True, required=False,
    )

    firstname = schema.TextLine(
        title=_(u"First name")
    )

    lastname = schema.TextLine(
        title=_(u"Last name")
    )

    salutation = schema.TextLine(
        title=_(u"Preferred salutation"),
        missing_value=u"",
        required=False
    )

    description = schema.Text(
        title=_(u"Introduction"),
        missing_value=u"",
        required=False
    )

    form.widget(groups=CheckBoxFieldWidget)
    groups = schema.List(
        title=_(u"Groups"),
        value_type=schema.Choice(
            title=_("Group"),
            vocabulary="collective.roster.localgroups"
        ),
        min_length=1,
        required=True
    )

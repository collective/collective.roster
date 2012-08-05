# -*- coding: utf-8 -*-
"""Schemas"""

from zope import schema

from plone.directives import form

from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
_ = ZopeMessageFactory("jyu.roster")


class IRoster(form.Schema):
    """Personnel roster"""


class IPerson(form.Schema):
    """A person"""

    title = schema.TextLine(
        title=_(u"Title"),
        readonly=True, required=False,
        )

    firstname = schema.TextLine(
        title=_(u"First name")
        )

    lastname= schema.TextLine(
        title=_(u"Last name")
        )

    salutation = schema.TextLine(
        title=_(u"Preferred salutation"),
        missing_value = u"",
        required=False
        )

    description = schema.Text(
        title=_(u"Introduction"),
        missing_value = u"",
        required = False
        )

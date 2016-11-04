# -*- coding: utf-8 -*-
"""Personnel roster and person related interfaces and schemas
"""
from collective.roster import _
from os import path
from plone.app.textfield import RichText
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from plone.supermodel.directives import primary
from z3c.form.validator import SimpleFieldValidator
from z3c.form.validator import WidgetsValidatorDiscriminators
from z3c.form.validator import WidgetValidatorDiscriminators
from zope import schema
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import Invalid

import magic


class discriminators(object):
    """Z3C Form validator discriminator decorator
    """
    def __init__(self, **kw):
        self.kw = kw

    def __call__(self, cls):
        if 'schema' in self.kw:
            WidgetsValidatorDiscriminators(cls, **self.kw)
        else:
            WidgetValidatorDiscriminators(cls, **self.kw)
        return cls


class IRoster(model.Schema):
    """Content schema
    """
    columns_display = schema.List(
        title=_(u'Display columns'),
        description=_(u'Display only the selected person information columns '
                      u'on supporting views.'),
        value_type=schema.Choice(
            title=_(u'Column'),
            vocabulary='collective.roster.displaycolumns',
        )
    )


class IPersonnelListing(Interface):
    """Marker interface
    """


class IPerson(model.Schema):
    """Content schema
    """
    title = schema.TextLine(
        title=_(u'Display name'),
        readonly=True,
        required=False
    )

    first_name = schema.TextLine(
        title=_(u'First name')
    )

    last_name = schema.TextLine(
        title=_(u'Last name')
    )

    position = schema.TextLine(
        title=_(u'Title'),
        missing_value=u'',
        required=False
    )

    description = schema.Text(
        title=_(u'Description'),
        missing_value=u'',
        required=False
    )

    biography = RichText(
        title=_(u'Biography'),
        required=False
    )

    primary('image')
    image = NamedBlobImage(
        title=_(u'Image'),
        required=False
    )


@discriminators(field=IPerson['first_name'])
class FirstNameValidator(SimpleFieldValidator):
    def validate(self, value, force=False):
        normalizer = getUtility(IIDNormalizer)
        if not len(normalizer.normalize(value)):
            raise Invalid(_(u'Person name contains invalid characters.'))


@discriminators(field=IPerson['last_name'])
class LastNameValidator(SimpleFieldValidator):
    def validate(self, value, force=False):
        normalizer = getUtility(IIDNormalizer)
        if not len(normalizer.normalize(value)):
            raise Invalid(_(u'Person name contains invalid characters.'))


@discriminators(field=IPerson['image'])
class ImageFileValidator(SimpleFieldValidator):
    def validate(seflf, value, force=False):
        allowed = ['jpeg', 'jpg', 'png', 'gif']
        ext = path.splitext(value.filename)[1]
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(value.data)

        if (not ext or ext[1:].lower() not in allowed or not mime_type.startswith('image/')):  # noqa
            raise Invalid(_(u'Image must be one of the permitted file types '
                            u'(${extlist}).',
                            mapping={'extlist': u', '.join(allowed)}))


class IPersonTitle(Interface):
    """Adapter schema
    """

    def __str__():
        """Pre-formatted title"""

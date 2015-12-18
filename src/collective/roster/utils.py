# -*- coding: utf-8 -*-
""" Useful utility methods """

from Acquisition import aq_inner, aq_parent
from os import path
from zope.interface import Invalid
import magic

from collective.roster import _


def parents(context):
    """ Parents of the context

    Generator to walk the acquistion chain of object, considering that it
    could be a function.

    >>> for obj in self.parents:
    >>>    pass

    See: http://plone.org/documentation/manual/developer-manual/archetypes/
    appendix-practicals/b-org-creating-content-types-the-plone-2.5-way/
    writing-a-custom-pas-plug-in
    """
    context = aq_inner(context)

    while context is not None:
        yield context

        funcObject = getattr(context, "im_self", None)
        if funcObject is not None:
            context = aq_inner(funcObject)
        else:
            # Don't use aq_inner() since portal_factory (and probably other)
            # things, depends on being able to wrap itself in a fake context.
            context = aq_parent(context)


def getFirstParent(context, iface):
    for parent in parents(context):
        if iface.providedBy(parent):
            return parent
    return None


def validate_image_file_extension(value):
    allowed = ['jpeg', 'jpg', 'png', 'gif']
    ext = path.splitext(value.filename)[1]
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(value.data)

    if not ext or ext[1:].lower() not in allowed or not mime_type.startswith("image/"):
        raise Invalid(_(u"Image must be one of the permitted file types (${extlist}).",
                        mapping={"extlist": u", ".join(allowed)}))
    return True

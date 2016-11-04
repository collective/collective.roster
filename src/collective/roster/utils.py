# -*- coding: utf-8 -*-
import Acquisition


# noinspection PyUnresolvedReferences
def parents(context, iface=None):
    """Iterate through parents for the context (providing the given interface).

    Return generator to walk the acquisition chain of object, considering that
    it could be a function.

    Source: http://plone.org/documentation/manual/developer-manual/archetypes/
    appendix-practicals/b-org-creating-content-types-the-plone-2.5-way/
    writing-a-custom-pas-plug-in
    """
    context = Acquisition.aq_inner(context)

    while context is not None:
        if iface.providedBy(context):
            yield context

        funcObject = getattr(context, 'im_self', None)
        if funcObject is not None:
            context = Acquisition.aq_inner(funcObject)
        else:
            # Don't use Acquisition.aq_inner() since portal_factory (and
            # probably other) things, depends on being able to wrap itself in a
            # fake context.
            context = Acquisition.aq_parent(context)

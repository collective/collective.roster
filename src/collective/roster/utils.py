# -*- coding: utf-8 -*-
from Products.CMFPlone.CatalogTool import num_sort_regex
from Products.CMFPlone.CatalogTool import zero_fill
from Products.CMFPlone.utils import safe_callable
from Products.CMFPlone.utils import safe_unicode

import Acquisition
import locale


# http://bo.geekworld.dk/the-scandinavian-curse-sorting-ae-o-and-a/
def sortable_title(obj):
    title = getattr(obj, 'Title', None)
    if title is not None:
        if safe_callable(title):
            title = title()

        if isinstance(title, basestring):
            sortabletitle = safe_unicode(title).lower().strip()
            sortabletitle = num_sort_regex.sub(zero_fill, sortabletitle)
            sortabletitle = sortabletitle[:70].encode('utf-8')
            return locale.strxfrm(sortabletitle)

    return ''


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

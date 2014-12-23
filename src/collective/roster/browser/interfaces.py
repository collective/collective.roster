# -*- coding: utf-8 -*-
from z3c.form.interfaces import IFormLayer
from zope.viewlet.interfaces import IViewletManager


class IRosterLayer(IFormLayer):
    """Browser layer
    """


class IRosterViewlets(IViewletManager):
    """Marker interface
    """


class IPersonViewlets(IViewletManager):
    """Marker interface
    """

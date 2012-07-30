from persistent import Persistent
from zope.annotation import factory
from zope.interface import alsoProvides, implements
from zope.component import adapts

from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from jyu.roster import _



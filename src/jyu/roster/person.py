from five import grok

from zope import schema
from zope.interface import Interface
from z3c.form import button

from plone.directives import form, dexterity
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

#from Products.statusmessages.interfaces import IStatusMessage

from zope.interface import Invalid

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
import plone.app.vocabularies
from zope.component import adapts
from z3c.form.interfaces import IEditForm, IAddForm
from zope.interface import alsoProvides, implements

from rwproperty import getproperty, setproperty

from jyu.roster import _


class RolesVocabulary(grok.GlobalUtility):
    grok.provides(IVocabularyFactory)
    grok.name("jyu.roster.roles")

    def __call__(self, context):
       # if IRoster.providedBy(context):
        #    # find out the list of categories
        #    
        # How to get the parent folder of context?
        # from Acquisition import aq_parent, aq_inner
       # parent = aq_parent(aq_inner(context))

       # if IRoster.providedBy(parent):
        #    # find out the list of categories
        #   
        #else:
        return SimpleVocabulary([])

        roles = SimpleVocabulary(
            [SimpleTerm(value=u'Author', title=_(u'Author')),
             SimpleTerm(value=u'Referee', title=_(u'Referee')),
             SimpleTerm(value=u'Guest Editor', title=_(u'Guest Editor')),
             SimpleTerm(value=u'Editorial Board Member', title=_(u'Editorial Board Member'))]
            )
        return roles

#grok.global_utility(RolesVocabulary, name=u'jyu.roster.roles')

class IPerson(form.Schema):
    """A person in the roster. 
    """

    title = schema.TextLine(
            title=_(u"Full Name"),
			description=_(u"First name and last name"),
        )

    salutation = schema.TextLine(
            title=_(u"Preferred Salutation"),
            description=_(u"For example: Mr., Dr., Mrs., etc."),
            required=False,
        )

    keywords = schema.Text(
            title=_(u"Your Research Keywords"),
        )

    

"""  picture = NamedImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
        )
"""


class IPortalRoles(form.Schema):
   
        
    portalroles = schema.Tuple(
        title=_(u"Portal Roles"),
            value_type=schema.Choice(
                vocabulary="plone.app.vocabularies.Roles",
            ),
        required=False,
    )

    #this puts field after all the standard fields of content type
    form.order_after(portalroles = '*')
       
    form.omitted('portalroles')
    form.no_omit(IEditForm, 'portalroles')
    form.no_omit(IAddForm, 'portalroles')

alsoProvides(IPortalRoles, form.IFormFieldProvider)

class IPortalRolesMarker(Interface):
    """Marker interface for portal roles viewlet, etc..."""

class MetadataBase(object):
    
    adapts(IDexterityContent)
    
    def __init__(self, context):
        self.context = context

_marker = object()

class DCFieldProperty(object):
    def __init__(self, field, get_name=None, set_name=None):
        if get_name is None:
            get_name = field.__name__
        self._field = field
        self._get_name = get_name
        self._set_name = set_name

    def __get__(self, inst, klass):
        if inst is None:
            return self

        attribute = getattr(inst.context, self._get_name, _marker)
        if attribute is _marker:
            field = self._field.bind(inst)
            attribute = getattr(field, 'default', _marker)
            if attribute is _marker:
                raise AttributeError(self._field.__name__)
        elif callable(attribute):
            attribute = attribute()

        if isinstance(attribute, DateTime):
            # Ensure datetime value is stripped of any timezone and seconds
            # so that it can be compared with the value returned by the widget
            return datetime(*map(int, attribute.parts()[:6]))
        return attribute

    def __set__(self, inst, value):
        field = self._field.bind(inst)
        field.validate(value)
        if field.readonly:
            raise ValueError(self._field.__name__, 'field is readonly')
        if isinstance(value, datetime):
            # The ensures that the converted DateTime value is in the
            # server's local timezone rather than GMT.
            value = DateTime(value.year, value.month, value.day,
                             value.hour, value.minute)
        if self._set_name:
            getattr(inst.context, self._set_name)(value)
        elif inst.context.hasProperty(self._get_name):
            inst.context._updateProperty(self._get_name, value)
        else:
            setattr(inst.context, self._get_name, value)

    def __getattr__(self, name):
        return getattr(self._field, name)


class PortalRoles(object):
   
    implements(IPortalRoles)

    def __init__(self, context):
        self.context = context
    
    @getproperty
    def portalroles(self):
        return set(self.context.Subject())

    @setproperty
    def portalroles(self,value):
        if value is None:
            value = ()
        self.context.setSubject(tuple(value))

#    def _get_subjects(self):
 #       return self.context.subject
  #  def _set_subjects(self, value):
   #     self.context.subject = value
    #subjects = property(_get_subjects, _set_subjects)


class View(grok.View):

    grok.context(IPerson)
    grok.require('zope2.View')
    grok.name('view')


 
    
from plone.app.viewletmanager.manager import OrderedViewletManager


class PersonViewletManager(OrderedViewletManager, grok.ViewletManager):
    grok.context(IPerson)
    grok.name("jyu.roster.person")


class PersonDetailsViewlet(grok.Viewlet):
   grok.context(IPerson)
   grok.viewletmanager(PersonViewletManager)
   grok.name("jyu.roster.person.details")


class PortalRolesViewlet(grok.Viewlet):
   grok.context(IPortalRolesMarker)
   grok.viewletmanager(PersonViewletManager)
   grok.name("jyu.roster.person.rolesview")


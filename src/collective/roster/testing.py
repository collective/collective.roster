# -*- coding: utf-8 -*-
"""Test layer"""

from Acquisition import aq_base
from ZODB.POSException import ConflictError

from zope.component import getSiteManager
from OFS.SimpleItem import SimpleItem

from plone.app.testing import (
    PloneSandboxLayer,
    applyProfile,
    FunctionalTesting,
    PLONE_FIXTURE,
)

from plone.testing.z2 import ZSERVER_FIXTURE

from Products.MailHost.interfaces import IMailHost
from Products.CMFPlone.tests.utils import MockMailHost


class RosterLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.roster
        self.loadZCML(package=collective.roster)

    def setUpPloneSite(self, portal):
        # Set our Robot Framework remote library
        portal._setObject("RosterRemoteLibrary", RemoteLibrary())

        # Replace MailHost with MockMailHost
        portal._original_MailHost = portal.MailHost
        portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

        applyProfile(portal, 'collective.roster:default')

    def tearDownPloneSite(self, portal):
        # Remove our Robot Framework remote library
        portal._delObject("RosterRemoteLibrary")

        # Restore the original MailHost
        portal.MailHost = portal._original_MailHost
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(portal._original_MailHost),
                           provided=IMailHost)

ROSTER_FIXTURE = RosterLayer()

ROSTER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(ROSTER_FIXTURE, ZSERVER_FIXTURE),
    name="Acceptance")


class RemoteLibrary(SimpleItem):
    """Robot Framework Remote Library"""

    def get_keyword_names(self):
        """ """
        keywords = Keywords()
        names = filter(lambda x: x[0] != "_", dir(keywords))
        return names

    def run_keyword(self, name, args):
        """ """
        keywords = Keywords()
        func = getattr(keywords, name)
        result = {"error": "", "return": ""}
        try:
            retval = func(*args)
        except Exception, e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        else:
            result["status"] = "PASS"
            result["return"] = retval
        return result


class Keywords(object):

    def product_has_been_activated(self, product_name):
        from zope.component.hooks import getSite
        from Products.CMFCore.utils import getToolByName

        quickinstaller = getToolByName(getSite(), "portal_quickinstaller")

        assert quickinstaller.isProductInstalled(product_name)

    def create_form_letter_template(self, title, retry=3):
        from zope.component import getUtility
        from zope.component.hooks import getSite
        from plone.i18n.normalizer.interfaces import IURLNormalizer
        from plone.dexterity.utils import createContentInContainer

        if not type(title) == unicode:
            title = unicode(title, "utf-8")

        portal = getSite()
        if portal:
            portal._p_jar.sync()

            name = getUtility(IURLNormalizer).normalize(title)
            createContentInContainer(portal, 'collective.roster.template',
                                     checkConstraints=False, id=str(name))

            obj = portal[name]

            from plone.app.dexterity.behaviors.metadata import IBasic
            IBasic(obj).title = unicode(title)
            IBasic(obj).description = u"This is a form letter template"

            obj.header_from = u"nobody@collective.fi"
            obj.header_to = [u"plone-support@collective.fi"]
            obj.header_subject = u"Important message"
            obj.body = u"Important message from ${absolute_url}."

            obj.reindexObject()

        try:
            from transaction import commit
            commit()
        except ConflictError:
            if retry:
                self.create_form_letter_template(title, max(0, retry - 1))



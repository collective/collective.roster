# -*- coding: utf-8 -*-
""" Test layer """

from Acquisition import aq_base
from ZODB.POSException import ConflictError

from zope.component import getSiteManager
from OFS.SimpleItem import SimpleItem

from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,

    applyProfile,

    IntegrationTesting,
    FunctionalTesting,
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

ROSTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ROSTER_FIXTURE, ),
    name="Functional")

ROSTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ROSTER_FIXTURE, ),
    name="Functional")

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

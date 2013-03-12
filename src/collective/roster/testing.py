from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
    applyProfile
)
from plone.testing import z2

from Products.MailHost.interfaces import IMailHost
from Products.CMFPlone.tests.utils import MockMailHost
from Acquisition import aq_base

from zope.component import getSiteManager
from OFS.SimpleItem import SimpleItem


class Layer(PloneSandboxLayer):
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

ROSTER_FIXTURE = Layer()

ROSTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ROSTER_FIXTURE,), name="Integration")

ROSTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ROSTER_FIXTURE,), name="Functional")


class RobotLayer(PloneSandboxLayer):
    defaultBases = (ROSTER_FIXTURE,)

    def setUpPloneSite(self, portal):
        from collective.roster.testing_robot import RemoteKeywordsLibrary
        portal._setObject("RemoteKeywordsLibrary", RemoteKeywordsLibrary())

    def tearDownPloneSite(self, portal):
        portal._delObject("RemoteKeywordsLibrary")


ROBOT_FIXTURE = RobotLayer()

ROBOT_TESTING = FunctionalTesting(
    bases=(ROBOT_FIXTURE, z2.ZSERVER_FIXTURE), name="Robot")

# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
    applyProfile,
    ploneSite
)
from plone.testing import (
    z2,
    Layer
)
from zope.component import getSiteManager


class RosterLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.roster
        self.loadZCML(package=collective.roster)

    def setUpPloneSite(self, portal):
        # Replace MailHost with MockMailHost
        portal._original_MailHost = portal.MailHost
        portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

        applyProfile(portal, 'collective.roster:default')

    def tearDownPloneSite(self, portal):
        # Restore the original MailHost
        portal.MailHost = portal._original_MailHost
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(portal._original_MailHost),
                           provided=IMailHost)

ROSTER_FIXTURE = RosterLayer()

ROSTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ROSTER_FIXTURE,), name="Integration")

ROSTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ROSTER_FIXTURE,), name="Functional")


class RobotLayer(Layer):
    defaultBases = (ROSTER_FIXTURE,)

    def setUp(self):
        from collective.roster.testing_robot import RemoteKeywordsLibrary
        with ploneSite() as portal:
            portal._setObject("RemoteKeywordsLibrary", RemoteKeywordsLibrary())

    def tearDown(self):
        with ploneSite() as portal:
            portal._delObject("RemoteKeywordsLibrary")

ROSTER_ROBOT_FIXTURE = RobotLayer()

ROSTER_ROBOT_TESTING = FunctionalTesting(
    bases=(ROSTER_ROBOT_FIXTURE, z2.ZSERVER_FIXTURE), name="Robot")

# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
    applyProfile
)
from plone.testing import z2
from zope.component import getSiteManager


class Layer(PloneSandboxLayer):
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


ROSTER_ROBOT_FIXTURE = RobotLayer()

ROSTER_ROBOT_TESTING = FunctionalTesting(
    bases=(ROSTER_ROBOT_FIXTURE, z2.ZSERVER_FIXTURE), name="Robot")

# -*- coding: utf-8 -*-
from plone.app.testing import (
    PloneSandboxLayer,
    PLONE_FIXTURE,
    IntegrationTesting,
    FunctionalTesting,
    applyProfile,
)
from plone.testing import (
    z2,
)
from plone.app.robotframework.testing import (
    MOCK_MAILHOST_FIXTURE,
    REMOTE_LIBRARY_BUNDLE_FIXTURE
)


class RosterLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.roster
        self.loadZCML(package=collective.roster)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.roster:default')

ROSTER_FIXTURE = RosterLayer()

ROSTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ROSTER_FIXTURE,), name="Integration")

ROSTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ROSTER_FIXTURE,), name="Functional")

ROSTER_ROBOT_TESTING = FunctionalTesting(
    bases=(MOCK_MAILHOST_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           ROSTER_FIXTURE,
           z2.ZSERVER_FIXTURE), name="Robot")

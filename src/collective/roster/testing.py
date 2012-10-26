# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

# from plone.testing import z2


class RosterConfiguredFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.roster
        self.loadZCML(package=collective.roster)

    def setUpPloneSite(self, portal):
        pass

ROSTER_CONFIGURED_FIXTURE = RosterConfiguredFixture()

ROSTER_CONFIGURED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ROSTER_CONFIGURED_FIXTURE,),
    name="RosterConfiguredFixture:Integration")
ROSTER_CONFIGURED_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ROSTER_CONFIGURED_FIXTURE,),
    name="RosterConfiguredFixture:Functional")

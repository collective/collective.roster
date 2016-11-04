# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import MOCK_MAILHOST_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class RosterLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)

        import collective.roster
        self.loadZCML(package=collective.roster)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.roster:default')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

ROSTER_FIXTURE = RosterLayer()

ROSTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ROSTER_FIXTURE,), name='Integration')

ROSTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ROSTER_FIXTURE,), name='Functional')

ROSTER_ACCEPTANCE_TESTING = ROSTER_ROBOT_TESTING = FunctionalTesting(
    bases=(MOCK_MAILHOST_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           ROSTER_FIXTURE,
           z2.ZSERVER_FIXTURE), name='Robot')

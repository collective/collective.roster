#-*- coding: utf-8 -*-
import unittest2 as unittest
from corejet.core import Scenario, story, scenario, given, when, then

import transaction

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles

from plone.testing import z2

from collective.roster.testing import ROSTER_CONFIGURED_FUNCTIONAL_TESTING


@story(id="30278553", title=u"As a user, I want to add a new personnel roster")
class Story(unittest.TestCase):

    layer = ROSTER_CONFIGURED_FUNCTIONAL_TESTING

    def setUp(self):
        self.browser = z2.Browser(self.layer["app"])

    @property
    def portal(self):
        return self.layer["portal"]

    @property
    def portal_url(self):
        return self.portal.absolute_url()

    @scenario(u"Roster product can be activated for the site")
    class Scenario(Scenario):

        @given(u"I've logged in")
        def givenA(self):
            self.browser.open(self.portal_url + "/login_form")
            self.browser.getControl("Login Name").value = TEST_USER_NAME
            self.browser.getControl("Password").value = TEST_USER_PASSWORD
            self.browser.getControl("Log in").click()

            self.assertFalse(
                self.portal.portal_membership.isAnonymousUser(),
                u"I'm anonymous, so I'm not logged in yet.")

        @given(u"I have 'Manager' role")
        def givenB(self):
            mtool = self.portal.portal_membership

            setRoles(self.portal, TEST_USER_ID, ["Manager"])
            transaction.commit()

            self.assertIn(
                "Manager",
                mtool.getAuthenticatedMember().getRoles(),
                u"I don't have 'Manager' role.")

        @when(u"I open the Add-ons form from the Plone Site Setup")
        def when(self):
            self.browser.open(self.portal_url + "/prefs_install_products_form")

        @then(u"'Personnel Roster' is available to be added")
        def then(self):
            self.assertIn(u"Personnel Roster", self.browser.contents,
                          u"'Personnel Roster' not found on Add-ons from.")

# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.roster.testing import ROSTER_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.roster is properly installed."""

    layer = ROSTER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.roster is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.roster'))

    def test_browserlayer(self):
        """Test that IROSTERLayer is registered."""
        from collective.roster.browser.interfaces import IRosterLayer
        from plone.browserlayer import utils
        self.assertIn(IRosterLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = ROSTER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

        # Uninstall as Manager
        setRoles(self.portal, TEST_USER_ID, ('Manager',))
        login(self.portal, TEST_USER_NAME)
        self.installer.uninstallProducts(['collective.roster'])

    def test_product_uninstalled(self):
        """Test if collective.roster is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.roster'))

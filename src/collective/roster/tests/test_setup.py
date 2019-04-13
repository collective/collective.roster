# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.roster.testing import ROSTER_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.roster is properly installed."""

    layer = ROSTER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.roster is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.roster'))

    def test_browserlayer(self):
        """Test that IRosterLayer is registered."""
        from collective.roster.browser.interfaces import IRosterLayer
        from plone.browserlayer import utils
        self.assertIn(IRosterLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = ROSTER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.roster'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.roster is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.roster'))

    def test_browserlayer_removed(self):
        """Test that IRosterLayer is removed."""
        from collective.roster.browser.interfaces import IRosterLayer
        from plone.browserlayer import utils
        self.assertNotIn(IRosterLayer, utils.registered_layers())

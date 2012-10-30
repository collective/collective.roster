# -*- coding: utf-8 -*-
"""Acceptance test suite"""

import unittest

from plone.testing import layered

from collective.roster.testing import ROSTER_ACCEPTANCE_TESTING
import robotsuite


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("acceptance"),
        layer=ROSTER_ACCEPTANCE_TESTING),
    ])
    return suite

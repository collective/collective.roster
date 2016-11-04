# -*- coding: utf-8 -*-
from collective.roster.testing import ROSTER_ACCEPTANCE_TESTING
from plone.testing import layered

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('acceptance'),
                layer=ROSTER_ACCEPTANCE_TESTING),
    ])
    return suite

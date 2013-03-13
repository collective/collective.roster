# -*- coding: utf-8 -*-
import robotsuite
import unittest
from collective.roster.testing import ROSTER_ROBOT_TESTING
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("acceptance"),
                layer=ROSTER_ROBOT_TESTING),
    ])
    return suite

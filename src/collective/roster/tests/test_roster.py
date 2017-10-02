# -*- coding: utf-8 -*-
from collective.roster.testing import ROSTER_INTEGRATION_TESTING

import unittest2 as unittest


class RosterIntegrationTests(unittest.TestCase):

    layer = ROSTER_INTEGRATION_TESTING

    def setUp(self):
        from plone.dexterity.utils import createContentInContainer
        portal = self.layer['portal']
        data = {
            'id': 'example-roster',
            'groups': [
                u'Title only',
                u'Alfa|Alfa coders',
                u'Beta|Beta testers',
                u'gamma-tester|Gamma Tester',
                u'delta tester|Delta Tester',
            ]
        }
        createContentInContainer(portal, 'collective.roster.roster',
                                 checkConstraints=False, **data)
        self.roster = portal['example-roster']

    def testRosterLocalGroupsVocabulary(self):
        from collective.roster.behaviors.groups import LocalGroupsVocabulary

        vocabulary = LocalGroupsVocabulary()(self.roster)

        self.assertEqual(len(vocabulary), 5)

        def to_tuple(term):
            return term.value, term.token, term.title

        tuples = map(to_tuple, vocabulary)

        self.assertIn((u'Title only', 'title-only', u'Title only'), tuples)
        self.assertIn((u'Alfa', 'alfa', u'Alfa coders'), tuples)
        self.assertIn((u'Beta', 'beta', u'Beta testers'), tuples)
        self.assertIn((u'gamma-tester', 'gamma-tester', u'Gamma Tester'), tuples)  # noqa: E501
        self.assertIn((u'delta tester', 'delta-tester', u'Delta Tester'), tuples)  # noqa: E501

    def testRosterDisplayColumnsVocabulary(self):
        from collective.roster.roster import DisplayColumnsVocabulary
        vocabulary = DisplayColumnsVocabulary()(self.roster)

        self.assertNotEqual(len(vocabulary), 0)

        def to_tuple(term):
            return term.value, term.token, term.title
        tuples = map(to_tuple, vocabulary)

        self.assertIn(('collective.roster.personnellisting.name',
                       'collective.roster.personnellisting.name',
                       u'Name'), tuples)

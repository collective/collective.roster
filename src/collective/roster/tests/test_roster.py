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
            'groups': [u'Alfa|Alfa coders', u'Beta|Beta testers']
        }
        createContentInContainer(portal, 'collective.roster.roster',
                                 checkConstraints=False, **data)
        self.roster = portal['example-roster']

    def testRosterLocalGroupsVocabulary(self):
        from collective.roster.behaviors.groups import LocalGroupsVocabulary

        vocabulary = LocalGroupsVocabulary()(self.roster)

        self.assertEqual(len(vocabulary), 2)

        def to_tuple(term):
            return term.value, term.token, term.title

        tuples = map(to_tuple, vocabulary)

        self.assertIn((u'Alfa', 'alfa-alfa-coders', u'Alfa coders'), tuples)
        self.assertIn((u'Beta', 'beta-beta-testers', u'Beta testers'), tuples)

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

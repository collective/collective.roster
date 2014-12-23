# -*- coding: utf-8 -*-
from borg.localrole.interfaces import ILocalRoleProvider
from zope.component import adapter
from zope.interface import implementer

from collective.roster.behaviors.interfaces import IAutoRoles


@adapter(ILocalRoleProvider)
@implementer(IAutoRoles)
class AutoRoleAdapter(object):
    _default_roles = ('Contributor', 'Editor', 'Reviewer')

    def __init__(self, context):
        self.context = context

    def getRoles(self, user_id):
        if user_id != self.context.getId():
            return ()
        else:
            return self._default_roles

    def getAllRoles(self):
        yield self.context.getId(), self._default_roles

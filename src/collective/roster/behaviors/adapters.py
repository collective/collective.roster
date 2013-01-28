# -*- coding: utf-8 -*-

from five import grok

from borg.localrole.interfaces import ILocalRoleProvider

from collective.roster.behaviors.interfaces import IAutoRoles


class AutoRoleAdapter(grok.Adapter):
    grok.provides(ILocalRoleProvider)
    grok.context(IAutoRoles)
    grok.name("person")

    _default_roles = ("Contributor", "Editor", "Reviewer")

    def __init__(self, context):
        self.context = context

    def getRoles(self, user_id):
        if user_id != self.context.getId():
            return ()
        else:
            return self._default_roles

    def getAllRoles(self):
        yield self.context.getId(), self._default_roles


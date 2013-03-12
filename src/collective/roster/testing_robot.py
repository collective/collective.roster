# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem

from plone import api
from Products.PluggableAuthService.plugins import DomainAuthHelper
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces


class KeywordsLibrary(object):

    def download_file(self, url):
        import urllib
        return urllib.urlopen(url).read()


class RemoteKeywordsLibrary(SimpleItem):
    """Robot Framework Remote Library Tool for Plone"""

    def get_keyword_names(self):
        """Return names of the implemented keywords
        """
        blacklist = dir(SimpleItem)
        blacklist.extend(['get_keyword_names', 'run_keyword',
                          'get_keyword_documentation', 'get_keyword_arguments'])
        names = filter(lambda x: x[0] != '_' and x not in blacklist, dir(self))
        return names

    def get_keyword_arguments(self, name):
        """Return keyword arguments
        """
        return None

    def get_keyword_documentation(self, name):
        """Return keyword documentation
        """
        func = getattr(self, name, None)
        return func.__doc__

    def run_keyword(self, name, args):
        """Execute the specified keyword with given arguments.
        """
        func = getattr(self, name, None)
        result = {'error': '', 'return': ''}
        try:
            retval = func(*args)
        except Exception, e:
            result['status'] = 'FAIL'
            result['error'] = str(e)
        else:
            result['status'] = 'PASS'
            result['return'] = retval
        return result

    def product_is_activated(self, product_name):
        """Assert that given product_name is activated in
        portal_quickinstaller.

        """
        from Products.CMFCore.utils import getToolByName
        quickinstaller = getToolByName(self, "portal_quickinstaller")
        assert quickinstaller.isProductInstalled(product_name),\
            "Product '%s' was not installed." % product_name

    def enable_autologin_as(self, *args):
        """Add and configure DomainAuthHelper PAS-plugin to login
        all anonymous users from localhost as a special *Remote User* with
        one or more given roles. Examples of use::

            Enable autologin as  Manager
            Enable autologin as  Site Administrator
            Enable autologin as  Member  Contributor

        """
        if "robot_login" in self.acl_users.objectIds():
            self.acl_users.robot_login._domain_map.clear()
        else:
            DomainAuthHelper.manage_addDomainAuthHelper(
                self.acl_users, "robot_login")
            activatePluginInterfaces(self, "robot_login")
        user = ", ".join(sorted(args))
        self.acl_users.robot_login.manage_addMapping(
            match_type="regex", match_string=".*", roles=args, username=user)

    def disable_autologin(self):
        """Clear DomainAuthHelper's map to effectively 'logout' user
        after 'autologin_as'. Example of use::

            Disable autologin

        """
        if "robot_login" in self.acl_users.objectIds():
            self.acl_users.robot_login._domain_map.clear()

    def add_user(self, email, fullname):
        """Add new user and add it to associate editors group."""
        properties = dict(fullname=fullname)
        user = api.user.create(email=email, properties=properties)
        api.group.add_user(groupname='associate-editors', user=user)

    def get_the_last_sent_email(self):
        """Return the last sent email"""
        return self.MailHost.messages[-1]

    def create_discussion_submission(self):
        """Create new discussion submission."""
        container = self.get('under-review')
        submission = api.content.create(
            type="jyu.simplejournalsystem.publication",
            title="Simplejournal publication",
            container=container)
        api.content.transition(obj=submission,
                               transition='accept_to_discussion_paper')

    def get_associate_editor(self):
        """Return associate editor info."""

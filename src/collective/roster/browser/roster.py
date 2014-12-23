# -*- coding: utf-8 -*-
import os
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.viewlet.viewlet import ViewletBase
from plone import api
from plone.memoize import view
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import getUtility

from collective.roster.roster import PersonnelAlphaListing


class DisplayViewsViewlet(ViewletBase):
    index = ViewPageTemplateFile(os.path.join(
        'templates', 'roster_displayviews_viewlet.pt'))

    def available(self):
        return len(self.menuItems) > 1

    @property
    @view.memoize
    def menuItems(self):
        menu = getUtility(IBrowserMenu, name='plone_displayviews')
        return sorted(menu.getMenuItems(self.context, self.request),
                      key=lambda item: item['action'])

    def render(self):
        return self.index()


class AlphaView(BrowserView):
    @property
    @view.memoize
    def table(self):
        table = PersonnelAlphaListing(self.context, self.request)
        table.update()
        table.render()  # table must be rendered once to count alphas
        return table

    @property
    @view.memoize
    def links(self):
        url = api.portal.getRequest().getURL()
        template = u'<a class="alpha-anchor" href="{0:s}#{1:s}">{2:s}</a>'
        return u'\n'.join([template.format(url, alpha, alpha)
                           for alpha in self.table.alpha])

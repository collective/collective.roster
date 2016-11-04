# -*- coding: utf-8 -*-
from collective.roster.roster import PersonnelAlphaListing
from plone import api
from plone.memoize import view
from Products.CMFDynamicViewFTI.interfaces import ISelectableBrowserDefault
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.viewlet.viewlet import ViewletBase
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import getUtility

import os


class DisplayViewsViewlet(ViewletBase):
    index = ViewPageTemplateFile(os.path.join(
        'templates', 'roster_displayviews_viewlet.pt'))

    def available(self):
        return len(self.menuItems) > 1

    @property
    @view.memoize
    def menuItems(self):
        menu = getUtility(IBrowserMenu, name='plone_displayviews')
        layouts = ISelectableBrowserDefault(self.context).getAvailableLayouts()
        actions = [layout[0] for layout in layouts]
        items = menu.getMenuItems(self.context, self.request)
        return sorted([item for item in items
                       if item['action'].strip('@') in actions],
                      key=lambda x: x['action'])

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

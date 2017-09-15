# -*- coding: utf-8 -*-

from z3c.form.interfaces import HIDDEN_MODE
from Products.CMFPlone.controlpanel.browser.site import SiteControlPanel as BaseSiteControlPanel  # noqa
from Products.CMFPlone.controlpanel.browser.site import SiteControlPanelForm as BaseSiteControlPanelForm  # noqa


class SiteControlPanelForm(BaseSiteControlPanelForm):

    def updateWidgets(self):
        super(SiteControlPanelForm, self).updateWidgets()
        # Hide the basic webstats_js field
        self.widgets['webstats_js'].mode = HIDDEN_MODE


class SiteControlPanel(BaseSiteControlPanel):
    """
    """
    form = SiteControlPanelForm

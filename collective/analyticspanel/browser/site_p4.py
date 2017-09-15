# -*- coding: utf-8 -*-

from zope.formlib.form import FormFields
from plone.app.controlpanel.site import ISiteSchema
from plone.app.controlpanel.site import SiteControlPanel as BaseSiteControlPanel


class SiteControlPanel(BaseSiteControlPanel):
    """
    Hide the basic webstats_js field
    """

    form_fields = FormFields(ISiteSchema).omit('webstats_js')


# -*- coding: utf-8 -*-
from collective.analyticspanel import messageFactory as _
from collective.analyticspanel.interfaces import IAnalyticsAdvancedSettings
from collective.analyticspanel.interfaces import IAnalyticsSettings
from collective.analyticspanel.interfaces import IAnalyticsSettingsSchema
from collective.analyticspanel.widgets.blockdatagridfield import (
    BlockDataGridFieldFactory,
)
from plone.app.registry.browser import controlpanel
from z3c.form import field, button
from z3c.form import group
from Products.statusmessages.interfaces import IStatusMessage


class FormAdvanced(group.Group):
    label = _("Advanced settings")
    fields = field.Fields(IAnalyticsAdvancedSettings)


class AnalyticsSettingsEditForm(controlpanel.RegistryEditForm):
    """Media settings form."""

    schema = IAnalyticsSettingsSchema
    fields = field.Fields(IAnalyticsSettings)
    fields["error_specific_code"].widgetFactory = BlockDataGridFieldFactory
    fields["path_specific_code"].widgetFactory = BlockDataGridFieldFactory

    groups = (FormAdvanced,)
    id = "AnalyticsSettingsEditForm"
    label = _("Analytics settings")
    description = _(
        "help_analytics_settings_editform",
        default="Manage JavaScript code and analytics snippets inclusion for the site",
    )

    @button.buttonAndHandler(_("Save"), name="save")
    def handleSave(self, action):
        keys = [x for x in self.request.form.keys()]
        for k in keys:
            if ".AA" in k:
                self.request.form[k.replace(".AA", ".0")] = self.request.form[k]
                del self.request.form[k]
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_("Changes saved"), "info")
        self.context.REQUEST.RESPONSE.redirect("@@analytics-settings")

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_("Edit cancelled"), "info")
        self.request.response.redirect(
            "%s/%s" % (self.context.absolute_url(), self.control_panel_view)
        )


class AnalyticsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Analytics settings control panel."""

    form = AnalyticsSettingsEditForm

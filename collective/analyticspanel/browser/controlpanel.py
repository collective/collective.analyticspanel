# -*- coding: utf-8 -*-

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from collective.analyticspanel import messageFactory as _
from collective.analyticspanel.interfaces import IAnalyticsSettings, IAnalyticsAdvancedSettings
from collective.analyticspanel.interfaces import IAnalyticsSettingsSchema
from plone.app.registry.browser import controlpanel
from z3c.form import button
from z3c.form import field
from z3c.form import group


def fix_widget_style(widget):
    widget.style = u'width: 100%';
    widget.klass += u" autoresize";
    widget.rows = 7


class FormAdvanced(group.Group):
    label = _(u"Advanced settings")
    fields = field.Fields(IAnalyticsAdvancedSettings)


class AnalyticsSettingsEditForm(controlpanel.RegistryEditForm):
    """Media settings form.
    """
    schema = IAnalyticsSettingsSchema
    fields = field.Fields(IAnalyticsSettings)
    groups = (FormAdvanced,)
    id = "AnalyticsSettingsEditForm"
    label = _(u"Analytics settings")
    description = _(u"help_analytics_settings_editform",
                    default=u"Manage JavaScript code and analytics snippets inclusion for the site")

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@analytics-settings")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


    def updateWidgets(self):
        super(AnalyticsSettingsEditForm, self).updateWidgets()
        fix_widget_style(self.widgets['general_code'])
        fix_widget_style(self.widgets['general_header_code'])
        for main_widget in self.widgets['error_specific_code'].widgets:
            error_widgets = main_widget.subform.widgets
            fix_widget_style(error_widgets['message_snippet'])
        for main_widget in self.widgets['path_specific_code'].widgets: 
            path_widgets = main_widget.subform.widgets
            path_widgets['path'].style = u'width: 100%'
            fix_widget_style(path_widgets['path_snippet'])


class AnalyticsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Analytics settings control panel.
    """
    form = AnalyticsSettingsEditForm
    #index = ViewPageTemplateFile('controlpanel.pt')


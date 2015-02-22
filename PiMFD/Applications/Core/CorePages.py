# coding=utf-8
"""
Holds system pages for use in the system application.
"""
from time import strftime, gmtime

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Text import SpacerLine


__author__ = 'Matt Eland'


class SysExitPage(MFDPage):
    """
    The exit Pi_MFD confirm page. Allows users to double select to quit the app.
    """

    def __init__(self, controller, application):
        super(SysExitPage, self).__init__(controller, application)

        header = self.get_header_label("Exit Application")
        confirm = self.get_label("Confirm exit by re-selecting '" + self.get_button_text() + "'")

        self.panel.children = [header, confirm]

    def get_button_text(self):
        """
        Gets the button text
        :return: The button text.
        """
        return "EXIT"

    def handle_reselected(self):
        """
        Handles the reselected event of the page.
        """
        self.controller.requested_exit = True


class DashboardPage(MFDPage):
    """
    A system clock page displaying the time in GMT and the current time zone.
    """

    def __init__(self, controller, application, time_data_provider):
        super(DashboardPage, self).__init__(controller, application)

        header = self.get_header_label("Current Time")
        self.lbl_sys_time = self.get_label("SYS: {}")
        self.lbl_gmt_time = self.get_label("GMT: {}")

        header_alerts = self.get_header_label("Alerts")
        self.lbl_alerts = self.get_label("No Alerts")
        
        self.time_data_provider = time_data_provider

        self.panel.children = [header,
                               self.lbl_sys_time,
                               self.lbl_gmt_time,
                               SpacerLine(self.display, self),
                               header_alerts,
                               self.lbl_alerts]

    def get_button_text(self):
        """
        Gets the button text.
        :return: The button text.
        """
        return "ALRT"

    def arrange(self):

        # Grab the time and stick it in the labels
        self.lbl_sys_time.text_data = self.time_data_provider.system_time
        self.lbl_gmt_time.text_data = self.time_data_provider.gmt_time

        return super(DashboardPage, self).arrange()



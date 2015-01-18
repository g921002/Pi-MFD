# coding=utf-8
"""
Holds system pages for use in the system application.
"""
from time import strftime, gmtime
import platform

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Rendering import render_text


__author__ = 'Matt Eland'


class SysRootPage(MFDPage):
    """
    The root level page for the system app
    """

    def get_button_text(self):
        """
        Gets the button text for the application
        :return: the button text for the application
        """
        return "SYS"  # Though this shouldn't get invoked since it's not going to be available

    def render(self, display):
        """
        Renders the page.
        :type display: PiMFD.DisplayManager.DisplayManager The DisplayManager that manages the page we're rendering.
        """
        super(SysRootPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        opts = self.controller.options

        # App Version
        y += render_text(display, font, opts.app_name + " Information", x, y,
                         cs.highlight).height + display.padding_y
        y += render_text(display, font, "   Ver: " + opts.app_version, x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, " Legal: Copyright (c) " + opts.app_author + " " + str(
            opts.copyright_year), x, y, cs.foreground).height + display.padding_y

        # Separator Line
        y += display.get_spacer_line_height()

        # System Data - TODO: These can be long and will need truncated or wrapping in some cases
        y += render_text(display, font, "System Information", x, y, cs.highlight).height + display.padding_y
        y += render_text(display, font,
                         'System: ' + platform.platform() + ' ' + platform.release() + ' ' + platform.machine(), x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, '  Proc: ' + platform.processor(), x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, 'Net ID: ' + platform.node(), x, y, cs.foreground).height + display.padding_y
        y += render_text(display, font, '  Disp: ' + str(self.display.res_x) + 'x' + str(self.display.res_y), x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font,
                         'Python: ' + platform.python_version() + ' ' + platform.python_implementation() + ' ' + platform.python_compiler(),
                         x, y, cs.foreground).height + display.padding_y


class SysExitPage(MFDPage):
    """
    The exit Pi_MFD confirm page. Allows users to double select to quit the app.
    """

    def get_button_text(self):
        """
        Gets the button text
        :return: The button text.
        """
        return "EXIT"

    def render(self, display):
        """
        Renders the exit page.
        :param display: The DisplayManager used to manage the display.
        """
        super(SysExitPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        if not self.controller.requested_exit:
            rect = render_text(display, font, "Exit Application", x, y, cs.highlight)
            y = rect.bottom + display.padding_y

            render_text(display, font, "Confirm exit by re-selecting '" + self.get_button_text() + "'", x, y,
                        cs.foreground)
        else:
            render_text(display, font, "The application will now close.", x, y, cs.foreground)

    def handle_reselected(self):
        """
        Handles the reselected event of the page.
        """
        self.controller.requested_exit = True


class SysClockPage(MFDPage):
    """
    A system clock page displaying the time in GMT and the current time zone.
    """
    
    def get_button_text(self):
        """
        Gets the button text.
        :return: The button text.
        """
        return "TIME"

    def render(self, display):
        """
        Renders the system clock page.
        :param display: The DisplayManager.
        """
        super(SysClockPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        y += render_text(display, font, "Current Time", x, y, cs.highlight).height + display.padding_y
        y += render_text(display, font, strftime("SYS: " + self.controller.time_format), x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, strftime("GMT: " + self.controller.time_format, gmtime()), x, y,
                         cs.foreground).height + display.padding_y


class SettingsPage(MFDPage):
    """
    A page for viewing and managing user settings
    """

    chk_scanline = None
    ddl_color_scheme = None
    num_zipcode = None

    def __init__(self, controller, application):
        super(SettingsPage, self).__init__(controller, application)

    def render(self, display):
        """
        Renders the page.
        :param display: The DisplayManager.
        """
        super(SettingsPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        opts = self.controller.options

        y += render_text(display, font, "Settings", x, y, cs.highlight).height + display.padding_y
        y += render_text(display, font, "Zip Code: {}".format(opts.location), x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, "Color Scheme: {}".format(cs.name), x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, "Scanline: {}".format(opts.enable_scan_line), x, y,
                         cs.foreground).height + display.padding_y

    def get_button_text(self):
        """
        Gets the button text.
        :return: The button text.
        """
        return "OPTS"


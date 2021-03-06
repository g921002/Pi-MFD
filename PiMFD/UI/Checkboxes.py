# coding=utf-8

"""
Contains checkbox style controls for manipulating pages
"""
from pygame.rect import Rect

from PiMFD.UI import Keycodes
from PiMFD.UI.Focus import FocusableWidget
from PiMFD.UI.Keycodes import is_enter_key
from PiMFD.UI.Panels import UIWidget, StackPanel
from PiMFD.UI.Rendering import render_rectangle
from PiMFD.UI.Text import TextBlock


__author__ = 'Matt Eland'


class CheckBoxGlyph(UIWidget):
    """
    A checkbox style UI without a label associated with it. This is used by other controls to render a checkbox UI.
    Use CheckBox instead if you're wanting to put this on a page.
    """

    checked = False
    render_focus = False
    check_pad = 4

    def __init__(self, display, page, checked=False):
        super(CheckBoxGlyph, self).__init__(display, page)
        self.checked = checked

    def arrange(self):
        rect_size = self.display.fonts.normal.size + self.check_pad

        self.desired_size = rect_size, rect_size

        return super(CheckBoxGlyph, self).arrange()

    def render(self):
        """
        Renders the glyph and returns its dimensions
        :return: The dimensions of the glyph
        """

        # Size Constants
        rect_size = self.display.fonts.normal.size + self.check_pad

        self.rect = Rect(self.pos[0], self.pos[1], self.desired_size[0], self.desired_size[1])

        focus_color = self.display.color_scheme.get_focus_color(self.render_focus)

        # Draw the border
        render_rectangle(self.display, focus_color, self.rect)

        # Draw checkmark (if checked)
        if self.checked:
            checked_rect = Rect(self.pos[0] + self.check_pad,
                                self.pos[1] + self.check_pad,
                                rect_size - (self.check_pad * 2),
                                rect_size - (self.check_pad * 2))

            render_rectangle(self.display, focus_color, checked_rect, width=0)

        # Update and return our dimensions
        return self.set_dimensions_from_rect(self.rect)


class CheckBox(FocusableWidget):
    """
    A CheckBox with an associated label.
    """

    text = None
    panel = None
    label = None
    glyph = None
    checked = False

    def __init__(self, display, page, label):
        super(CheckBox, self).__init__(display, page)

        self.text = label
        self.label = TextBlock(display, page, label)
        self.glyph = CheckBoxGlyph(display, page)

        self.panel = StackPanel(display, page, is_horizontal=True)
        self.panel.center_align = True
        self.panel.children = [self.label, self.glyph]

    def arrange(self):

        self.desired_size = self.panel.arrange()

        return super(CheckBox, self).arrange()

    def render(self):
        """
        Renders the checkbox with its current state
        :return: The rectangle of the checkbox
        """

        # Pass along our values to the children
        self.label.text = self.text
        self.glyph.checked = self.checked

        # Render the panel's contents
        self.panel.set_dimensions_from(self)
        self.panel.render()

        return self.set_dimensions_from(self.panel)

    def got_focus(self):
        """
        Occurs when the control gets focus
        """
        self.label.is_highlighted = True
        self.glyph.render_focus = True
        super(CheckBox, self).got_focus()

    def lost_focus(self):
        """
        Occurs when the control loses focus
        """
        self.label.is_highlighted = False
        self.glyph.render_focus = False
        super(CheckBox, self).lost_focus()

    def handle_key(self, key):
        """
        Handles a keypress
        :param key: The keycode
        :returns: True if the event was handled; otherwise False
        """

        if is_enter_key(key) or key == Keycodes.KEY_SPACE:

            if self.checked:
                self.checked = False
            else:
                self.checked = True

            self.state_changed()

            return True

        else:
            return super(CheckBox, self).handle_key(key)

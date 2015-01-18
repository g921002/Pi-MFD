# coding=utf-8
"""
Contains code useful for rendering lines of text
"""
from pygame.rect import Rect

from PiMFD.UI.Panels import UIWidget
from PiMFD.UI.Rendering import render_text


__author__ = 'Matt Eland'


class TextBlock(UIWidget):
    """
    Represents a segment of text
    """

    font = None
    text = None
    text_data = None
    is_highlighted = False

    def __init__(self, display, text, is_highlighted=False):
        super(TextBlock, self).__init__(display)
        self.font = display.font_normal
        self.text = text
        self.is_highlighted = is_highlighted

    def get_foreground(self):
        """
        Gets the calculated foreground color based on the label's attributes and the current color scheme.
        By having foreground be calculated like this, it provides a poor man's binding system where we can
        always grab the correct color from the color scheme, even when the color scheme changes.
        :return: The foreground
        """
        cs = self.display.color_scheme

        if self.is_highlighted:
            return cs.highlight
        else:
            return cs.foreground

    def render(self):
        """
        Renders the textblock to the default surface using the current properties of this object
        :rtype : RectType
        """

        self.left = self.pos[0]
        self.top = self.pos[1]

        # Do string formatting as needed
        effective_text = self.text
        if self.text is not None:
            if isinstance(self.text_data, tuple):
                effective_text = self.text.format(*self.text_data)
            else:
                effective_text = self.text.format(self.text_data)

        if self.font is not None and effective_text is not None:
            color = self.get_foreground()
            self.rect = render_text(self.display, self.font, effective_text, self.pos[0], self.pos[1], color)
        else:
            self.rect = Rect(self.left, self.top, 0, 0)

        return self.set_dimensions_from_rect(self.rect)
# coding=utf-8

"""
This file will hold map pages
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.Applications.Navigation.MapRendering import MapRenderer
from PiMFD.UI import Keycodes
from PiMFD.UI.Keycodes import is_up_key, is_right_key, is_left_key, is_down_key

__author__ = 'Matt Eland'


class MapPage(MFDPage):

    lbl_loading = None
    map_renderer = None
    context = None

    def __init__(self, controller, application):
        super(MapPage, self).__init__(controller, application)

        self.map_renderer = MapRenderer(application.map, controller.display, application.map_context)
        self.context = application.map_context

    def get_button_text(self):
        return self.application.map_context.active_filter.get_button_text()

    def render(self):

        if self.application.map.has_data:
            self.map_renderer.render()
        else:
            self.center_text('NO DATA')

        return super(MapPage, self).render()

    def handle_reselected(self):
        self.application.next_map_mode()
        super(MapPage, self).handle_reselected()

    def handle_key(self, key):

        if key == Keycodes.KEY_KP_PLUS or key == Keycodes.KEY_PLUS:
            self.application.zoom_in()
            return True

        elif key == Keycodes.KEY_KP_MINUS or key == Keycodes.KEY_MINUS:
            self.application.zoom_out()
            return True

        elif is_up_key(key):
            self.context.move_up()
            return True

        elif is_right_key(key):
            self.context.move_right()
            return True

        elif is_down_key(key):
            self.context.move_down()
            return True

        elif is_left_key(key):
            self.context.move_left()
            return True

        return super(MapPage, self).handle_key(key)


class MapInfoPage(MFDPage):
    lbl_header = None
    map_context = None

    def __init__(self, controller, application):
        super(MapInfoPage, self).__init__(controller, application)

        self.map_context = application.map_context
        self.lbl_header = self.get_header_label('Node Info')
        self.panel.children = [self.lbl_header]

    def render(self):
        return super(MapInfoPage, self).render()

    def get_button_text(self):
        return "INFO"

    def handle_selected(self):

        name = self.map_context.target.get_display_name()
        if name:
            self.lbl_header.text = name + " Info"
        else:
            self.lbl_header.text = "Node Info"

        super(MapInfoPage, self).handle_selected()






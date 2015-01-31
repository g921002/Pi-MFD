# coding=utf-8
from datetime import datetime
from time import strftime

from PiMFD.Applications.Navigation.MapSymbols import MapSymbol


__author__ = 'Matt Eland'

class MapRenderer(object):  # TODO: Maybe this should be a UIWidget?
    """
    A class used to render a Map object
    """

    def __init__(self, map, display, map_context, size=(200, 200)):
        self.map = map
        self.display = display
        self.center = ((display.res_x / 2.0), (display.res_y / 2.0))
        self.size = size
        self.map_context = map_context
        self.osm_shapes = None
        self.last_translate = None

    def render(self):

        # Smart scale the size to accomodate for the greatest dimension. This lets us support many aspect ratios.
        max_available = max(self.display.res_x, self.display.res_y)

        # Only recompute the expensive stuff if the resolution has changed or the data fetch time has changed
        if max_available != self.size[0] or \
                not self.last_translate or \
                        self.map.last_data_received > self.last_translate:

            # Recompute our dimensions
            self.size = (max_available, max_available)
            self.center = ((self.display.res_x / 2.0), (self.display.res_y / 2.0))

            # Translate the various curves, etc. into their appropraite screen positions
            self.osm_shapes = self.map.translate_shapes(self.size, self.center)

            self.last_translate = datetime.now()

        map_context = self.map_context

        # Render the open street map data
        if self.osm_shapes:
            for shape in self.osm_shapes:
                shape.render(self.display, map_context)

        # Render custom annotations over everything - these should always be recomputed
        if self.map.annotations:
            for annotation in self.map.annotations:
                sym = MapSymbol(annotation.lat, annotation.lng)
                sym.copy_values_from(annotation)
                pos = self.map.set_screen_position(annotation, self.size, self.center)
                sym.x, sym.y = pos
                sym.add_tag('incident', annotation.incident_type)
                if annotation.end:
                    sym.add_tag('end_date', strftime('%m/%d/%Y', annotation.end))
                if annotation.start:
                    sym.add_tag('start_date', strftime('%m/%d/%Y', annotation.start))
                sym.add_tag('note', annotation.description)
                sym.add_tag('severity', annotation.severity)
                sym.render(self.display, map_context)

        # Add ourself to the map - TODO: Add this to the annotation layer
        me = self.build_symbol(self.display.options.lat, self.display.options.lng)
        me.name = 'ME'
        me.add_tag('actor', 'self')
        me.add_tag('iff', 'self')
        me.render(self.display, map_context)

        # Draw the cursor as needed
        if self.map_context.should_show_cursor():
            cur = self.build_symbol(0, 0)
            cur.should_translate = False
            cur.set_pos(self.map_context.maintain_cursor_position())
            cur.add_tag('actor', 'cursor')
            cur.add_tag('owner', me.name)
            cur.add_tag('iff', 'self')
            rel_lat, rel_lng = self.map.translate_x_y_to_lat_lng(cur.x, cur.y,
                                                                 self.map.get_dimension_coefficients(self.size),
                                                                 self.center)
            cur.name = '{} , {}'.format(rel_lat, rel_lng)

            cur.render(self.display, map_context)

    def build_symbol(self, lat, lng):
        sym = MapSymbol(lat, lng)
        sym.x, sym.y = self.map.gps_to_screen(lat, lng, self.size, self.center)
        return sym

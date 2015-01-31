# coding=utf-8

"""
Contains classes used to hold map entities
"""
from PiMFD.Applications.Navigation.MapColoring import MapColorizer

__author__ = 'Matt Eland'


class MapEntity(object):
    """
    An abstract component present for maps
    """

    has_lines = False
    name = None
    tags = list()
    lat = 0.0
    lng = 0.0
    id = None
    points = None
    should_translate = True
    x = 0
    y = 0

    def __init__(self, lat, lng):
        super(MapEntity, self).__init__()

        self.tags = list()
        self.lat = lat
        self.lng = lng

    def get_tags(self, name):
        """
        Gets all tags that have name as their key
        :type name: str
        :param name: The tag key
        :return: All tags (yielded) that have the matching name
        """

        for tag in self.tags:
            if tag[0] == name:
                yield tag

    def has_tag(self, name):
        """
        Returns True if a tag with a key of name was found, regardless of value
        :param name: The key to look for
        :return: True if a tag with a key of name was found, otherwise False
        """

        for tag in self.get_tags(name):
            return True

        return False

    def get_tag_value(self, name):
        """
        Gets the value for the first tag that matches name or returns None
        :type name: str
        :param name: The tag key
        :return: The value for the first tag that matches name or returns None
        """

        for tag in self.get_tags(name):
            return tag[1]

        return None

    def calculate_lat_lng_from_points(self):

        if not self.points or len(self.points) < 1:
            return

        max_lat = self.points[0][0]
        min_lat = self.points[0][0]
        min_lng = self.points[0][1]
        max_lng = self.points[0][1]

        for point in self.points:
            min_lat = min(point[0], min_lat)
            max_lat = max(point[0], max_lat)
            min_lng = min(point[1], min_lng)
            max_lng = max(point[1], max_lng)

        self.lat = min_lat + ((max_lat - min_lat) / 2.0)
        self.lng = min_lng + ((max_lng - min_lng) / 2.0)

    def has_tag_value(self, name, value):
        """
        Determins if the specified tag / value pair exists in this set
        :type name: str
        :param name: The tag key
        :type value: str
        :param value: The tag value
        :return: True if the key / value pair was present, otherwise False
        """

        for tag in self.get_tags(name):
            if tag[1] == value:
                return True

        return False

    def get_color(self, cs):
        return MapColorizer.get_color(self, cs)

    def get_display_name(self):

        display_name = self.get_tag_value('short_name')
        if not display_name and self.name:
            display_name = self.abbreviate(self.name)

        return display_name

    @staticmethod
    def abbreviate(name, pretty=False):
        """
        Abbreviates a string by intelligently removing middle words and using the first initial
        """

        if name is None:
            return None

        # For / deliminated / multi-role establishments, just take the first chunk
        if '/' in name:
            return MapEntity.abbreviate(name[0:(name.index('/'))])
        elif '\\' in name:
            return MapEntity.abbreviate(name[0:(name.index('\\'))])

        # If we're a long name and we have a 's in the name, chop everything else after that
        if len(name) >= 10 and "'s" in name:
            return name[0:(name.index("'s") + 2)]

        names = name.split()

        # Just two words, don't abbreviate
        if len(names) <= 2:
            return name

        # Chop off silly opening words
        if names[0].lower() == 'the' or names[0].lower() == 'le' or names[0].lower() == 'la' or names[
            0].lower() == 'el':
            names = names[1:]
            return MapEntity.abbreviate(' '.join(names), pretty)

        result = [names[0]]
        tiny_name = False

        for surname in names[1:-1]:
            if len(surname) <= 3:
                result.append(surname)
                tiny_name = True
            else:
                if pretty and tiny_name:
                    result.append(surname)
                else:
                    result.append(surname[0] + '.')
                tiny_name = False

        result.append(names[-1])

        return ' '.join(result)

    def set_pos(self, pos):
        self.x, self.y = pos

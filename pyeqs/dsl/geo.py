# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class GeoDistance(dict):

    def __init__(self, coordinates, distance):
        """
        Geo Distance Filter

        Acceptable Input Styles:
        GeoDistance({'lat': 40, 'lon': -70}, '10km')
        GeoDistance({'lat': 40, 'lng': -70}, '10km')
        GeoDistance([40, -70], '10km')
        GeoDistance("-70,40", '10km')
        """
        super(GeoDistance, self).__init__()
        self.coordinates = self._parse_coordinates(coordinates)
        self.distance = distance
        self["geo_distance"] = self._build_dict()

    def _build_dict(self):
        geo_distance = {
            "distance": self.distance,
            "location": {
                'lat': self.coordinates[0],
                'lon': self.coordinates[1]
            }
        }
        return geo_distance

    def _parse_coordinates(self, coordinates):
        if isinstance(coordinates, list):
            lat = coordinates[1]
            lon = coordinates[0]
        if isinstance(coordinates, dict):
            lat = coordinates.pop('lat')
            lon = coordinates.values()[0]
        if isinstance(coordinates, (str, unicode)):
            lat, lon = coordinates.split(",")
        return map(float, [lat, lon])

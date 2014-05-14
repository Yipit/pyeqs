# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import GeoDistance
from tests.helpers import homogeneous


def test_add_geo_distance_with_dict():
    """
    Create Geo Distance with Dictionary
    """
    # When add a Geo Distance field
    t = GeoDistance({"lat": 1.0, "lon": 2.0}, "20mi")

    # Then I see the appropriate JSON
    results = {
        "geo_distance": {
            "distance": "20mi",
            "location": {
                "lat": 1.0,
                "lon": 2.0
            }
        }
    }

    homogeneous(t, results)


def test_add_geo_distance_with_string():
    """
    Create Geo Distance with String
    """
    # When add a Geo Distance field
    t = GeoDistance("1.0,2.0", "20mi")

    # Then I see the appropriate JSON
    results = {
        "geo_distance": {
            "distance": "20mi",
            "location": {
                "lat": 1.0,
                "lon": 2.0
            }
        }
    }

    homogeneous(t, results)


def test_add_geo_distance_with_array():
    """
    Create Geo Distance with Array
    """
    # When add a Geo Distance field
    t = GeoDistance([2.0, 1.0], "20mi")

    # Then I see the appropriate JSON
    results = {
        "geo_distance": {
            "distance": "20mi",
            "location": {
                "lat": 1.0,
                "lon": 2.0
            }
        }
    }

    homogeneous(t, results)

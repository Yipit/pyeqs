# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import GeoDistance
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_geo_distance_search_dict(context):
    """
    Perform search with geo distance filter with dictionary
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"location": {"lat": 1.1, "lon": 2.1}})
    add_document("foo", {"location": {"lat": 40.1, "lon": 80.1}})

    # And I filter for terms
    t.filter(GeoDistance({"lat": 1.0, "lon": 2.0}, "20mi"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_geo_distance_search_string(context):
    """
    Perform search with geo distance filter with string
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"location": {"lat": 1.1, "lon": 2.1}})
    add_document("foo", {"location": {"lat": 40.1, "lon": 80.1}})

    # And I filter for terms
    t.filter(GeoDistance("1.0,2.0", "20mi"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_geo_distance_search_array(context):
    """
    Perform search with geo distance filter with array
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"location": {"lat": 1.1, "lon": 2.1}})
    add_document("foo", {"location": {"lat": 40.1, "lon": 80.1}})

    # And I filter for terms
    t.filter(GeoDistance([2.0, 1.0], "20mi"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)

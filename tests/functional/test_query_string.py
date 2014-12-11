# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import QueryString
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_query_string(context):
    """
    Search with query string
    """
    # When I create a queryset with a query string
    qs = QueryString("cheese")
    t = QuerySet("localhost", index="foo", query=qs)

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "cheese"})

    # Then I get a the expected results
    results = t[0:10]
    len(results).should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_query_string_with_additional_parameters(context):
    """
    Search with query string and additional parameters
    """
    # When I create a queryset with parameters
    qs = QueryString("cheese", fields=["bar"], use_dis_max=False, tie_breaker=0.05)
    t = QuerySet("localhost", index="foo", query=qs)

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "cheese"})

    # Then I get a the expected results
    results = t[0:10]
    len(results).should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_query_string_with_different_parameters(context):
    """
    Search with query string and different parameters
    """
    # When I create a queryset with parameters
    qs = QueryString("cheese", default_field="bar", use_dis_max=False, tie_breaker=0.05)
    t = QuerySet("localhost", index="foo", query=qs)

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "cheese"})

    # Then I get a the expected results
    results = t[0:10]
    len(results).should.equal(1)

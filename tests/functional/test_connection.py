# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_simple_search_with_host_string(context):
    """
    Connect with host string
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})

    # And I do a search
    results = t[0:1]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})


@scenario(prepare_data, cleanup_data)
def test_simple_search_with_host_dict(context):
    """
    Connect with host dict
    """
    # When create a queryset
    connection_info = {"host": "localhost", "port": 9200}
    t = QuerySet(connection_info, index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})

    # And I do a search
    results = t[0:1]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})


@scenario(prepare_data, cleanup_data)
def test_simple_search_with_host_list(context):
    """
    Connect with host list
    """
    # When create a queryset
    connection_info = [{"host": "localhost", "port": 9200}]
    t = QuerySet(connection_info, index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})

    # And I do a search
    results = t[0:1]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})

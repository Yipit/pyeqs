# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Sort
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_with_asc_sorting(context):
    """
    Perform search with ascending sorting
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add sorting
    s = Sort("bar", order="asc")
    t.order_by(s)
    results = t[0:10]

    # Then my results have the proper sorting
    results[0]["_source"]["bar"].should.equal(1)
    results[1]["_source"]["bar"].should.equal(2)
    results[2]["_source"]["bar"].should.equal(3)


@scenario(prepare_data, cleanup_data)
def test_search_with_desc_sorting(context):
    """
    Perform search with descending sorting
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add sorting
    s = Sort("bar", order="desc")
    t.order_by(s)
    results = t[0:10]

    # Then my results have the proper sorting
    results[0]["_source"]["bar"].should.equal(3)
    results[1]["_source"]["bar"].should.equal(2)
    results[2]["_source"]["bar"].should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_search_with_mode_sorting(context):
    """
    Perform search with descending sorting and mode
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": [1, 10]})
    add_document("foo", {"bar": [2, 10]})
    add_document("foo", {"bar": [3, 10]})

    # And I add sorting
    s = Sort("bar", order="desc", mode="min")
    t.order_by(s)
    results = t[0:10]

    # Then my results have the proper sorting
    results[0]["_source"]["bar"].should.equal([3, 10])
    results[1]["_source"]["bar"].should.equal([2, 10])
    results[2]["_source"]["bar"].should.equal([1, 10])

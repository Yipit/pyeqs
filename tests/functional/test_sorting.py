# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Sort
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_with_asc_sorting(context):
    """
    Search with ascending sorting
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
    Search with descending sorting
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
    Search with descending sorting and mode
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


@scenario(prepare_data, cleanup_data)
def test_search_with_multiple_sorts(context):
    """
    Search with multiple sorts
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 10, "baz": 1})
    add_document("foo", {"bar": 10, "baz": 2})
    add_document("foo", {"bar": 10, "baz": 3})

    # And I add sorting
    first_sort = Sort("bar", order="asc")
    second_sort = Sort("baz", order="asc")
    t.order_by(first_sort)
    t.order_by(second_sort)
    results = t[0:10]

    # Then my results have the proper sorting
    results[0]["_source"]["baz"].should.equal(1)
    results[1]["_source"]["baz"].should.equal(2)
    results[2]["_source"]["baz"].should.equal(3)


@scenario(prepare_data, cleanup_data)
def test_search_with_missing_sort(context):
    """
    Search with 'missing' sort
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 10, "baz": 1})
    add_document("foo", {"bar": 10, "baz": 2})
    add_document("foo", {"bar": 10, "baz": None})

    # And I add sorting
    first_sort = Sort("bar", order="asc", missing='_first')
    t.order_by(first_sort)
    results = t[0:10]

    # Then my results have the proper sorting
    results[0]["_source"]["baz"].should.equal(1)
    results[1]["_source"]["baz"].should.equal(2)
    results[2]["_source"]["baz"].should.equal(None)

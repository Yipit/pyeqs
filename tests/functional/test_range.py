# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Range
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_with_lte_range(context):
    """
    Perform search with lte range filter
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add a range filter
    _type = Range("bar", lte=1)
    t.filter(_type)
    results = t[0:10]

    # Then my results only have that type
    len(results).should.equal(1)
    results[0]["_source"]["bar"].should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_search_with_lt_range(context):
    """
    Perform search with lt range filter
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add a range filter
    _type = Range("bar", lt=2)
    t.filter(_type)
    results = t[0:10]

    # Then my results only have that type
    len(results).should.equal(1)
    results[0]["_source"]["bar"].should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_search_with_gte_range(context):
    """
    Perform search with gte range filter
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add a range filter
    _type = Range("bar", gte=3)
    t.filter(_type)
    results = t[0:10]

    # Then my results only have that type
    len(results).should.equal(1)
    results[0]["_source"]["bar"].should.equal(3)


@scenario(prepare_data, cleanup_data)
def test_search_with_gt_range(context):
    """
    Perform search with gt range filter
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add a range filter
    _type = Range("bar", gt=2)
    t.filter(_type)
    results = t[0:10]

    # Then my results only have that type
    len(results).should.equal(1)
    results[0]["_source"]["bar"].should.equal(3)

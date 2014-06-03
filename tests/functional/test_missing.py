# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Missing
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_with_missing(context):
    """
    Search with missing
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"baz": 2})
    add_document("foo", {"bar": 3})

    # And I add filters
    t.filter(Missing("bar"))
    results = t[0:10]

    # Then my results are filtered correctly
    len(results).should.equal(1)
    results[0]["_source"]["baz"].should.equal(2)


@scenario(prepare_data, cleanup_data)
def test_search_with_missing_existence_null_value(context):
    """
    Search with missing via non-existence or a null value
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"baz": 2})
    add_document("foo", {"baz": 3, "bar": None})

    # And I add filters
    t.filter(Missing("bar", existence=True, null_value=True))
    results = t[0:10]

    # Then my results are filtered correctly
    len(results).should.equal(2)

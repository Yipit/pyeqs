# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Term
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_simple_search_with_filter(context):
    """
    Search with filter
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do a filtered search
    t.filter(Term("bar", "baz"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})


@scenario(prepare_data, cleanup_data)
def test_search_with_multiple_filters(context):
    """
    Search with multiple filters
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz", "foo": "foofoo"})

    # And I do a filtered search
    t.filter(Term("bar", "bazbaz"))
    t.filter(Term("foo", "foo"))
    results = t[0:10]

    # Then I get the appropriate response
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "bazbaz", "foo": "foo"})


@scenario(prepare_data, cleanup_data)
def test_search_with_filter_block(context):
    """
    Search with Filter Block
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz", "foo": "foofoo"})

    # And I do a filtered search
    f = Filter("or").filter(Term("bar", "baz")).filter(Term("foo", "foo"))
    t.filter(f)
    results = t[0:10]

    # Then I get the appropriate response
    len(results).should.equal(2)

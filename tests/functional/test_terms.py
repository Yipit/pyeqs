# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Terms
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_terms_search(context):
    """
    Search with terms filter
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz", "foo": "foo"})
    add_document("foo", {"bar": "baz", "foo": "foofoo"})
    add_document("foo", {"bar": "baz", "foo": "foofoofoo"})

    # And I filter for terms
    t.filter(Terms("foo", ["foo", "foofoo"]))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(3)


@scenario(prepare_data, cleanup_data)
def test_terms_search_with_execution(context):
    """
    Search with terms filter with execution
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"foo": ["foo", "bar"]})
    add_document("foo", {"foo": ["foo", "baz"]})

    # And I filter for terms
    t.filter(Terms("foo", ["foo", "bar"], execution="and"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]["_source"]["foo"].should.equal(["foo", "bar"])

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Term
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_simple_search(context):
    """
    Perform simple match_all search
    """
    # When create a queryset
    t = QuerySet("http://localhost:9200", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})

    # And I do a search
    results = t[0:1]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})


@scenario(prepare_data, cleanup_data)
def test_simple_search_with_filter(context):
    """
    Perform simple filtered search
    """
    # When create a queryset
    t = QuerySet("http://localhost:9200", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do a filtered search
    t.filter(Term("bar", "baz"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})

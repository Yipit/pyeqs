# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet, Bool
from pyeqs.dsl import Term
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_simple_search_with_boolean_must(context):
    """
    Search with boolean must
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do a filtered search
    b = Bool()
    b.must(Term("bar", "baz"))
    t.filter(b)
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})


@scenario(prepare_data, cleanup_data)
def test_simple_search_with_boolean_must_not(context):
    """
    Search with boolean must not
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do a filtered search
    b = Bool()
    b.must_not(Term("bar", "baz"))
    t.filter(b)
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "bazbaz"})


@scenario(prepare_data, cleanup_data)
def test_simple_search_with_boolean_should(context):
    """
    Search with boolean should
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do a filtered search
    b = Bool()
    b.should(Term("bar", "baz"))
    t.filter(b)
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})

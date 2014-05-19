# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Term, ScriptScore, Sort
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_simple_search(context):
    """
    Search with match_all query
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
def test_string_search(context):
    """
    Search with string query
    """
    # When create a queryset
    t = QuerySet("localhost", query="cheese", index="foo")

    # And there are records
    add_document("foo", {"bar": "banana"})
    add_document("foo", {"bar": "cheese"})

    # And I do a search
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "cheese"})


@scenario(prepare_data, cleanup_data)
def test_search_with_filter(context):
    """
    Search with match_all query and filter
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do a search
    t.filter(Term("bar", "baz"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})


@scenario(prepare_data, cleanup_data)
def test_search_with_filter_and_scoring(context):
    """
    Search with match_all query, filter and scoring
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "scoring_field": 1})
    add_document("foo", {"bar": "baz", "scoring_field": 2})
    add_document("foo", {"bar": "bazbaz", "scoring_field": 3})

    # And I do a search
    t.filter(Term("bar", "baz"))
    score = ScriptScore("final_score = 0 + doc['scoring_field'].value;")
    t.score(score)
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(2)
    results[0]['_source'].should.equal({"bar": "baz", "scoring_field": 2})
    results[1]['_source'].should.equal({"bar": "baz", "scoring_field": 1})


@scenario(prepare_data, cleanup_data)
def test_search_with_filter_and_scoring_and_sorting(context):
    """
    Search with match_all query, filter, scoring, and sorting
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "scoring_field": 0, "sorting_field": 30})
    add_document("foo", {"bar": "baz", "scoring_field": 1, "sorting_field": 20})
    add_document("foo", {"bar": "baz", "scoring_field": 2, "sorting_field": 10})
    add_document("foo", {"bar": "bazbaz", "scoring_field": 3, "sorting_field": 0})

    # And I do a search
    t.filter(Term("bar", "baz"))
    score = ScriptScore("final_score = 0 + doc['scoring_field'].value;")
    t.score(score)
    sorting = Sort("sorting_field", order="desc")
    t.order_by(sorting)
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(3)
    results[0]['_source'].should.equal({"bar": "baz", "scoring_field": 0, "sorting_field": 30})
    results[1]['_source'].should.equal({"bar": "baz", "scoring_field": 1, "sorting_field": 20})
    results[2]['_source'].should.equal({"bar": "baz", "scoring_field": 2, "sorting_field": 10})

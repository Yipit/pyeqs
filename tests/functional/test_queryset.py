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
def test_search_with_scoring_min_score_and_track_scores(context):
    """
    Search with match_all query and scoring with min_score and track_scores
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "scoring_field": 1})
    add_document("foo", {"bar": "baz", "scoring_field": 2})
    add_document("foo", {"bar": "baz", "scoring_field": 3})

    # And I do a search
    score = ScriptScore("final_score = 0 + doc['scoring_field'].value;")
    t.score(score, min_score=2, track_scores=True)
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(2)
    results[0]['_source'].should.equal({"bar": "baz", "scoring_field": 3})
    results[1]['_source'].should.equal({"bar": "baz", "scoring_field": 2})


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


@scenario(prepare_data, cleanup_data)
def test_search_with_filter_and_scoring_and_sorting_and_fields(context):
    """
    Search with match_all query, filter, scoring, sorting, and fields
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
    t.only(["bar"])
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(3)
    results[0]['fields'].should.equal({"bar": ["baz"]})
    results[1]['fields'].should.equal({"bar": ["baz"]})
    results[2]['fields'].should.equal({"bar": ["baz"]})


@scenario(prepare_data, cleanup_data)
def test_wrappers(context):
    """
    Search with wrapped match_all query
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I do a search
    def wrapper_function(search_results):
        return list(map(lambda x: x['_source']['bar'] + 1, search_results))
    t.wrappers(wrapper_function)
    t.order_by(Sort("bar", order="asc"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(3)
    results[0].should.equal(2)
    results[1].should.equal(3)
    results[2].should.equal(4)


@scenario(prepare_data, cleanup_data)
def test_search_as_queryset_with_filter(context):
    """
    Search with match_all query and filter on a cloned queryset
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do a filter on my new object
    my_search = t.objects.filter(Term("bar", "baz"))

    # And a different filter on my old object
    t.filter(Term("bar", "bazbaz"))

    # And I do a search
    results = my_search[0:10]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})


@scenario(prepare_data, cleanup_data)
def test_search_with_iterator(context):
    """
    Search using an iterator
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And set iterator fetching to a small size
    t._per_request = 2

    # And there are records
    add_document("foo", {"bar": 0})
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})
    add_document("foo", {"bar": 4})

    # And I do a filter on my new object

    # And a different filter on my old object
    t.order_by(Sort("bar", order="asc"))

    # Then I get the expected results
    for (counter, result) in enumerate(t):
        result['_source'].should.equal({"bar": counter})

    len(t).should.equal(5)
    t.count().should.equal(5)
    t.max_score().should_not.be(None)


@scenario(prepare_data, cleanup_data)
def test_post_query_actions(context):
    """
    Search with match_all query with post query actions
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I have a post query action
    global my_global_var
    my_global_var = 1

    def action(self, results, start, stop):
        global my_global_var
        my_global_var += 1

    t.post_query_actions(action)

    # And I do a search
    t.order_by(Sort("bar", order="asc"))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(3)
    results[0]["_source"]["bar"].should.equal(1)
    results[1]["_source"]["bar"].should.equal(2)
    results[2]["_source"]["bar"].should.equal(3)
    my_global_var.should.equal(2)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httpretty
import json

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Aggregations, QueryString, ScriptScore, Sort, Term, TermSuggesters
from tests.helpers import homogeneous


def test_create_queryset():
    """
    Create Default QuerySet
    """
    # When create a queryset
    t = QuerySet("foobar")

    # Then I see the appropriate JSON
    results = {
        "query": {"match_all": {}}
    }

    homogeneous(t._query, results)


def test_create_queryset_with_query_string():
    """
    Create QuerySet with QueryString
    """
    # When create a queryset
    q = QueryString("foo")
    t = QuerySet("foobar", query=q)

    # Then I see the appropriate JSON
    results = {
        "query": {
            "query_string": {
                "query": "foo"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_filter():
    """
    Create QuerySet with Filter
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add a filter
    t.filter(Term("foo", "bar"))

    # Then I see the appropriate JSON
    results = {
        "query": {
            "filtered": {
                "query": {"match_all": {}},
                "filter": {
                    "and": [
                        {
                            "term": {
                                "foo": "bar"
                            }
                        }
                    ]
                }
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_filters():
    """
    Create QuerySet with Multiple Filters
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add a filter
    t.filter(Term("foo", "bar"))
    t.filter(Term("foobar", "foobar"))

    # Then I see the appropriate JSON
    results = {
        "query": {
            "filtered": {
                "query": {"match_all": {}},
                "filter": {
                    "and": [
                        {
                            "term": {
                                "foo": "bar"
                            }
                        },
                        {
                            "term": {
                                "foobar": "foobar"
                            }
                        }
                    ]
                }
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_filter_block():
    """
    Create QuerySet with Filter Block
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add a filter
    f = Filter("or").filter(Term("foo", "bar"))
    t.filter(f)

    # Then I see the appropriate JSON
    results = {
        "query": {
            "filtered": {
                "query": {"match_all": {}},
                "filter": {
                    "or": [
                        {
                            "term": {
                                "foo": "bar"
                            }
                        }
                    ]
                }
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_sorting():
    """
    Create QuerySet with Sorting
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add sorting
    s = Sort("_id", order="asc")
    t.order_by(s)

    # Then I see the appropriate JSON
    results = {
        "query": {
            "match_all": {}
        },
        "sort": [
            {
                "_id": {
                    "order": "asc"
                }
            }
        ]
    }

    homogeneous(t._query, results)


def test_create_queryset_with_multiple_sorting():
    """
    Create QuerySet with Multiple Sorting
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add sorting
    s = Sort("_id", order="asc")
    t.order_by(s)

    ss = Sort("_id", order="desc")
    t.order_by(ss)

    # Then I see the appropriate JSON
    results = {
        "sort": [
            {
                "_id": {
                    "order": "asc"
                }
            },
            {
                "_id": {
                    "order": "desc"
                }
            }
        ],
        "query": {
            "match_all": {}
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_scoring():
    """
    Create QuerySet with Scoring
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s)

    # Then I see the appropriate JSON
    results = {
        "query": {
            "function_score": {
                "functions": [
                    {
                        "script_score": {
                            "script": "foo = 0.0"
                        }
                    }
                ],
                "query": {"match_all": {}},
                "boost_mode": "replace",
                "score_mode": "multiply"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_scoring_min_score_track_score():
    """
    Create QuerySet with Scoring, Minimum Score and Track Scores
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s, min_score=0, track_scores=True)

    # Then I see the appropriate JSON
    results = {
        "min_score": 0,
        "track_scores": True,
        "query": {
            "function_score": {
                "functions": [
                    {
                        "script_score": {
                            "script": "foo = 0.0"
                        }
                    }
                ],
                "query": {"match_all": {}},
                "boost_mode": "replace",
                "score_mode": "multiply"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_multiple_scoring():
    """
    Create QuerySet with Multiple Scoring
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s)

    # And I add more scoring
    boost = {
        "boost_factor": "3",
        "filter": Term("foo", "bar")
    }
    t.score(boost)

    # Then I see the appropriate JSON
    results = {
        "query": {
            "function_score": {
                "query": {"match_all": {}},
                "functions": [
                    {
                        "script_score": {
                            "script": "foo = 0.0"
                        }
                    },
                    {
                        "boost_factor": "3",
                        "filter": {
                            "term": {
                                "foo": "bar"
                            }
                        }
                    }
                ],
                "boost_mode": "replace",
                "score_mode": "multiply"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_scoring_and_filtering():
    """
    Create QuerySet with Scoring and Filtering
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s)

    # And I add filtering
    t.filter(Term("foo", "bar"))

    # Then I see the appropriate JSON
    results = {
        "query": {
            "function_score": {
                "query": {
                    "filtered": {
                        "query": {"match_all": {}},
                        "filter": {
                            "and": [
                                {
                                    "term": {
                                        "foo": "bar"
                                    }
                                }
                            ]
                        }
                    }
                },
                "functions": [
                    {
                        "script_score": {
                            "script": "foo = 0.0"
                        }
                    }
                ],
                "boost_mode": "replace",
                "score_mode": "multiply"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_scoring_and_filtering_from_object():
    """
    Create QuerySet with Scoring and Filter Object
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s)

    # And I add filtering
    f = Filter("and").filter(Term("foo", "bar"))
    t.filter(f)

    # Then I see the appropriate JSON
    results = {
        "query": {
            "function_score": {
                "query": {
                    "filtered": {
                        "query": {"match_all": {}},
                        "filter": {
                            "and": [
                                {
                                    "term": {
                                        "foo": "bar"
                                    }
                                }
                            ]
                        }
                    }
                },
                "functions": [
                    {
                        "script_score": {
                            "script": "foo = 0.0"
                        }
                    }
                ],
                "boost_mode": "replace",
                "score_mode": "multiply"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_filters_and_scoring():
    """
    Create QuerySet with Scoring and Multiple Filters
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add filtering
    t.filter(Term("foo", "bar"))

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s)

    # And I add a second filter
    t.filter(Term("foobar", "foobar"))

    # Then I see the appropriate JSON
    results = {
        "query": {
            "function_score": {
                "query": {
                    "filtered": {
                        "query": {"match_all": {}},
                        "filter": {
                            "and": [
                                {
                                    "term": {
                                        "foo": "bar"
                                    }
                                },
                                {
                                    "term": {
                                        "foobar": "foobar"
                                    }
                                }
                            ]
                        }
                    }
                },
                "functions": [
                    {
                        "script_score": {
                            "script": "foo = 0.0"
                        }
                    }
                ],
                "boost_mode": "replace",
                "score_mode": "multiply"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_only_block():
    """
    Create QuerySet with Only block
    """
    # When create a query block
    t = QuerySet("foobar")

    # And I add an 'only' block
    t.only("_id")

    # Then I see the appropriate JSON
    results = {
        "query": {"match_all": {}},
        "fields": ["_id"]
    }

    homogeneous(t._query, results)


def test_queryset_count():
    """
    Get QuerySet Count
    """
    # When I create a query block
    t = QuerySet("foobar")

    # Then I get an appropriate Count
    t.count().should.equal(None)


def test_queryset_max_score():
    """
    Get QuerySet Max Score
    """
    # When I create a query block
    t = QuerySet("foobar")

    # Then I get an appropriate max score
    t.max_score().should.equal(None)


def test_queryset_string():
    """
    Create QuerySet with String query
    """
    # When I create a query block
    t = QuerySet("foobar", query="foo")

    # Then I see the appropriate JSON
    results = {
        "query": {
            "query_string": {
                "query": "foo"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_aggregation():
    """
    Create QuerySet with an Aggregation
    """
    # When I create a query block
    t = QuerySet("foobar")

    # And I aggregate
    a = Aggregations("agg_name", "field_name", "metric")
    t.aggregate(a)

    results = {
        "query": {
            "match_all": {}
        },
        "aggregations": {
            "agg_name": {"metric": {"field": "field_name"}}
        }
    }
    homogeneous(t._query, results)

    # And I can do it as many times as I want
    a1 = Aggregations("other_agg_name", "other_field_name", "terms", size=1)
    t.aggregate(a1)

    results = {
        "query": {
            "match_all": {}
        },
        "aggregations": {
            "agg_name": {"metric": {"field": "field_name"}},
            "other_agg_name": {"terms": {
                "field": "other_field_name",
                "size": 1
            }}
        }
    }
    homogeneous(t._query, results)


def test_create_queryset_with_term_suggester():
    """
    Create QuerySet with a TermSuggester
    """
    # When I create a query block
    t = QuerySet("foobar")

    # And I suggest
    s = TermSuggesters("sugg_name", "text_content", "field_name")
    t.suggest(s)

    results = {
        "query": {
            "match_all": {}
        },
        "suggest": {
            "sugg_name": {
                "text": "text_content",
                "term": {
                    "field": "field_name", "max_edits": 2, "max_term_freq": 0.01,
                    "min_doc_freq": 0, "min_word_length": 4, "prefix_length": 1,
                    "sort": "score", "suggest_mode": "missing"
                }
            }
        }
    }

    homogeneous(t._query, results)

    # And I can do it as many times as I want
    s1 = TermSuggesters("other_sugg_name", "other_text_content", "other_field_name", size=7)
    t.suggest(s1)

    results = {
        "query": {
            "match_all": {}
        },
        "suggest": {
            "sugg_name": {
                "text": "text_content",
                "term": {
                    "field": "field_name", "max_edits": 2, "max_term_freq": 0.01,
                    "min_doc_freq": 0, "min_word_length": 4, "prefix_length": 1,
                    "sort": "score", "suggest_mode": "missing"
                }
            },
            "other_sugg_name": {
                "text": "other_text_content",
                "term": {
                    "field": "other_field_name", "max_edits": 2, "size": 7,
                    "max_term_freq": 0.01, "min_doc_freq": 0, "min_word_length": 4,
                    "prefix_length": 1, "sort": "score", "suggest_mode": "missing"}
            }
        }
    }
    homogeneous(t._query, results)


def test_create_queryset_with_global_term_suggester():
    """
    Create QuerySet with a global TermSuggester
    """
    # When I create a query block
    t = QuerySet("foobar")

    # And I suggest
    s = TermSuggesters("sugg_name", "text_content", "field_name", global_=True)
    t.suggest(s)

    results = {
        "query": {
            "match_all": {}
        },
        "suggest": {
            "text": "text_content",
            "sugg_name": {
                "term": {
                    "field": "field_name", "max_edits": 2, "max_term_freq": 0.01,
                    "min_doc_freq": 0, "min_word_length": 4, "prefix_length": 1,
                    "sort": "score", "suggest_mode": "missing"
                }
            }
        }
    }

    homogeneous(t._query, results)

    # And I can add nested ones
    s1 = TermSuggesters("other_sugg_name", "other_text_content", "other_field_name", size=7)
    t.suggest(s1)

    results = {
        "query": {
            "match_all": {}
        },
        "suggest": {
            "text": "text_content",
            "sugg_name": {
                "term": {
                    "field": "field_name", "max_edits": 2, "max_term_freq": 0.01,
                    "min_doc_freq": 0, "min_word_length": 4, "prefix_length": 1,
                    "sort": "score", "suggest_mode": "missing"
                }
            },
            "other_sugg_name": {
                "text": "other_text_content",
                "term": {
                    "field": "other_field_name", "max_edits": 2, "size": 7,
                    "max_term_freq": 0.01, "min_doc_freq": 0, "min_word_length": 4,
                    "prefix_length": 1, "sort": "score", "suggest_mode": "missing"}
            }
        }
    }
    homogeneous(t._query, results)


@httpretty.activate
def test_queryset_getitem():
    """
    Fetch from QuerySet with __getitem__
    """
    # When I create a query block
    t = QuerySet("localhost", index="bar")

    # And I have records
    response = {
       "took": 12,
       "hits": {
          "total": 1,
          "max_score": 10,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "1",
                "_score": 10,
                "_source": {
                   "foo": "bar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }
    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                       body=json.dumps(response),
                       content_type="application/json")

    results = t[0:1]
    len(results).should.equal(1)
    t.count().should.equal(1)


@httpretty.activate
def test_queryset_getitem_with_wrapper():
    """
    Fetch from QuerySet with __getitem__ and wrapper
    """
    # When I create a query block
    t = QuerySet("localhost", index="bar")
    wrapper = lambda y: list(map(lambda x: x['_id'], y))
    t.wrappers(wrapper)

    # And I have records
    response = {
       "took": 12,
       "hits": {
          "total": 1,
          "max_score": 10,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "1",
                "_score": 10,
                "_source": {
                   "foo": "bar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }
    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                       body=json.dumps(response),
                       content_type="application/json")

    results = t[0:1]
    len(results).should.equal(1)
    t.count().should.equal(1)
    t.max_score().should.equal(10)
    int(results[0]).should.equal(1)


@httpretty.activate
def test_queryset_getitem_multiple():
    """
    Fetch from QuerySet with __getitem__ multiple times
    """
    # When I create a query block
    t = QuerySet("localhost", index="bar")
    wrapper = lambda y: list(map(lambda x: x['_id'], y))
    t.wrappers(wrapper)
    # And I have a record
    response = {
       "took": 12,
       "hits": {
          "total": 1,
          "max_score": 10,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "1",
                "_score": 10,
                "_source": {
                   "foo": "bar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }
    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                       body=json.dumps(response),
                       content_type="application/json")

    results = t[0:1]
    len(results).should.equal(1)
    t.count().should.equal(1)

    results = t[0:1]
    len(results).should.equal(1)
    t.count().should.equal(1)


@httpretty.activate
def test_queryset_iteration():
    """
    Fetch results with QuerySet via __iter__
    """

    # When I create a query block
    t = QuerySet("foobar", index="bar")
    wrapper = lambda y: list(map(lambda x: x['_id'], y))
    t.wrappers(wrapper)

    # And I have a record
    response = {
       "took": 12,
       "hits": {
          "total": 1,
          "max_score": 10,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "1",
                "_score": 10,
                "_source": {
                   "foo": "bar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }
    httpretty.register_uri(httpretty.GET, "http://foobar:9200/bar/_search",
                       body=json.dumps(response),
                       content_type="application/json")

    results = []
    for result in t:
        results.append(result)
    len(results).should.equal(1)
    len(t).should.equal(1)
    t.count().should.equal(1)


@httpretty.activate
def test_queryset_iteration_with_no_results():
    """
    Fetch results with QuerySet via __iter__ with no results
    """

    # When I create a query block
    t = QuerySet("foobar", index="bar")
    wrapper = lambda y: list(map(lambda x: x['_id'], y))
    t.wrappers(wrapper)

    # And I have no records
    response = {
       "took": 12,
       "hits": {
          "total": 0,
          "max_score": 0,
          "hits": []
       }
    }
    httpretty.register_uri(httpretty.GET, "http://foobar:9200/bar/_search",
                       body=json.dumps(response),
                       content_type="application/json")

    results = []
    for result in t:
        results.append(result)
    len(results).should.equal(0)
    t.count().should.equal(0)


@httpretty.activate
def test_queryset_iteration_with_multiple_cache_fetches():
    """
    Fetch results with QuerySet via __iter__ with multiple cache fetches
    """

    # When I create a query block
    t = QuerySet("foobar", index="bar")
    wrapper = lambda y: list(map(lambda x: x['_id'], y))
    t.wrappers(wrapper)

    # And we lower the per request to force multiple fetches
    t._per_request = 2

    # And I have records
    first_response = {
       "took": 12,
       "hits": {
          "total": 3,
          "max_score": 10,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "1",
                "_score": 10,
                "_source": {
                   "foo": "bar"
                },
                "sort": [
                   1395687078000
                ]
             },
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "2",
                "_score": 10,
                "_source": {
                   "foo": "barbar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }

    second_response = {
       "took": 12,
       "hits": {
          "total": 3,
          "max_score": 10,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "3",
                "_score": 10,
                "_source": {
                   "foo": "barbarbar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }
    httpretty.register_uri(httpretty.GET, "http://foobar:9200/bar/_search",
                        responses=[
                           httpretty.Response(body=json.dumps(first_response), content_type="application/json"),
                           httpretty.Response(body=json.dumps(second_response), content_type="application/json"),
                        ])

    # Then I should eventually get all records
    results = []
    for result in t:
        results.append(result)
    len(results).should.equal(3)
    t.count().should.equal(3)
    results[0].should.equal("1")
    results[1].should.equal("2")
    results[2].should.equal("3")


@httpretty.activate
def test_queryset_getitem_with_post_query_action():
    """
    Fetch from QuerySet with __getitem__ and post query action
    """
    # When I create a query block
    t = QuerySet("localhost", index="bar")

    # And I have a post query action
    global my_global_var
    my_global_var = 1

    def action(self, results, start, stop):
        global my_global_var
        my_global_var += 1

    t.post_query_actions(action)

    # And I have records
    response = {
        "took": 12,
        "timed_out": False,
        "_shards": {
            "total": 5,
            "successful": 5,
            "failed": 0
        },
        "hits": {
            "total": 1,
            "max_score": 10,
            "hits": [
                {
                    "_index": "bar",
                    "_type": "baz",
                    "_id": "1",
                    "_score": 10,
                    "_source": {
                        "foo": "bar"
                    },
                    "sort": [
                        1395687078000
                    ]
                }
            ]
        }
    }
    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                       body=json.dumps(response),
                       content_type="application/json")

    results = t[0:1]
    len(results).should.equal(1)
    t.count().should.equal(1)

    # Then I see the correct results
    results[0]['_id'].should.equal('1')
    my_global_var.should.equal(2)


@httpretty.activate
def test_queryset_aggregations():
    """
    Fetch aggregation data from QuerySet with #aggregations
    """
    # When I create a query block
    t = QuerySet("localhost", index="bar")

    # And I aggregate something
    a = Aggregations("agg_name", "field_name", "metric")
    t.aggregate(a)

    # And I have records
    response = {
        "took": 12,
        "hits": {
            "total": 1,
            "max_score": 10,
            "hits": [
                {"_index": "bar",
                 "_type": "baz",
                 "_id": "1",
                 "_score": 10,
                 "_source": {
                     "foo": "bar"
                 },
                 "sort": [
                     1395687078000
                 ]}
            ]
        },
        "aggregations": {
            "agg_name": {"metric": {"field": "field_name"}}
        }
    }
    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                           body=json.dumps(response),
                           content_type="application/json")

    t[0:1]
    t.aggregations().should.have.key("agg_name").being.equal({"metric": {"field": "field_name"}})


@httpretty.activate
def test_queryset_suggestions():
    """
    Fetch suggest data from QuerySet with #suggestions
    """
    # When I create a query block
    t = QuerySet("localhost", index="bar")

    # And I suggest something
    s = TermSuggesters("sugg_name", "text_content", "field_name")
    t.suggest(s)

    # And I have records
    response = {
        "took": 12,
        "hits": {
            "total": 1,
            "max_score": 10,
            "hits": [
                {"_index": "bar",
                 "_type": "baz",
                 "_id": "1",
                 "_score": 10,
                 "_source": {
                     "foo": "bar"
                 },
                 "sort": [
                     1395687078000
                 ]}
            ]
        },
        "suggest": {
            "sugg_name": [
                {"text": "text_content", "offset": 0, "length": 13, "options": []}
            ]
        }
    }
    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                           body=json.dumps(response),
                           content_type="application/json")

    t[0:1]
    t.suggestions().should.have.key("sugg_name").being.equal([
        {"text": "text_content", "offset": 0, "length": 13, "options": []}
    ])

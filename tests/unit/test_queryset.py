# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httpretty
import json
import sure

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Term, Sort, ScriptScore
from tests.helpers import homogeneous


def test_create_queryset():
    """
    Create Default QuerySet
    """
    # When create a queryset
    t = QuerySet("http://foobar:9200")

    # Then I see the appropriate JSON
    results = {
        "query": {"match_all": {}}
    }

    homogeneous(t._query, results)


def test_create_queryset_with_filter():
    """
    Create QuerySet with Filter
    """
    # When create a query block
    t = QuerySet("http://foobar:9200")

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
    t = QuerySet("http://foobar:9200")

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
    t = QuerySet("http://foobar:9200")

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
    t = QuerySet("http://foobar:9200")

    # And I add sorting
    s = Sort("_id", order="asc")
    t.order_by(s)

    # Then I see the appropriate JSON
    results = {
        "sort": [
            {
                "_id": {
                    "order": "asc"
                }
            }
        ],
        "query": {
            "match_all": {}
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_multiple_sorting():
    """
    Create QuerySet with Multiple Sorting
    """
    # When create a query block
    t = QuerySet("http://foobar:9200")

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
    t = QuerySet("http://foobar:9200")

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s)

    # Then I see the appropriate JSON
    results = {
        "query": {
            "function_score": {
                "query": {"match_all": {}},
                "script_score": {
                    "script": "foo = 0.0"
                },
                "boost_mode": "replace"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_multiple_scoring():
    """
    Create QuerySet with Multiple Scoring
    """
    # When create a query block
    t = QuerySet("http://foobar:9200")

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s)

    # And I add more scoring
    ss = ScriptScore("foo = 1.0")
    t.score(ss)

    # Then I see the appropriate JSON
    results = {
        "query": {
            "function_score": {
                "query": {"match_all": {}},
                "script_score": {
                    "script": "foo = 1.0"
                },
                "boost_mode": "replace"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_scoring_and_filtering():
    """
    Create QuerySet with Scoring and Filtering
    """
    # When create a query block
    t = QuerySet("http://foobar:9200")

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
                "script_score": {
                    "script": "foo = 0.0"
                },
                "boost_mode": "replace"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_scoring_and_filtering_from_object():
    """
    Create QuerySet with Scoring and Filter Object
    """
    # When create a query block
    t = QuerySet("http://foobar:9200")

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
                "script_score": {
                    "script": "foo = 0.0"
                },
                "boost_mode": "replace"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_filtering_and_scoring():
    """
    Create QuerySet with Filtering and Scoring
    """
    # When create a query block
    t = QuerySet("http://foobar:9200")

    # And I add filtering
    t.filter(Term("foo", "bar"))

    # And I add scoring
    s = ScriptScore("foo = 0.0")
    t.score(s)

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
                "script_score": {
                    "script": "foo = 0.0"
                },
                "boost_mode": "replace"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_filters_and_scoring():
    """
    Create QuerySet with Scoring and Multiple Filters
    """
    # When create a query block
    t = QuerySet("http://foobar:9200")

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
                "script_score": {
                    "script": "foo = 0.0"
                },
                "boost_mode": "replace"
            }
        }
    }

    homogeneous(t._query, results)


def test_create_queryset_with_only_block():
    """
    Create QuerySet with Only block
    """
    # When create a query block
    t = QuerySet("http://foobar:9200")

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
    t = QuerySet("http://foobar:9200")

    # Then I get an appropriate Count
    t.count().should.equal(None)


def test_queryset_string():
    """
    Create QuerySet with String query
    """
    # When I create a query block
    t = QuerySet("http://foobar:9200", query="foo")

    # Then I see the appropriate JSON
    results = {
        "query": {
            "query_string": {
                "query": "foo"
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
    t = QuerySet("http://foobar:9200", index="bar")

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
    httpretty.register_uri(httpretty.GET, "http://foobar:9200/bar/_search",
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
    t = QuerySet("http://foobar:9200", index="bar")
    wrapper = lambda y: map(lambda x: x['_id'], y)
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
    httpretty.register_uri(httpretty.GET, "http://foobar:9200/bar/_search",
                       body=json.dumps(response),
                       content_type="application/json")

    results = t[0:1]
    len(results).should.equal(1)
    t.count().should.equal(1)
    int(results[0]).should.equal(1)


@httpretty.activate
def test_queryset_getitem_multiple():
    """
    Fetch from QuerySet with __getitem__ multiple times
    """
    # When I create a query block
    t = QuerySet("http://foobar:9200", index="bar")
    wrapper = lambda y: map(lambda x: x['_id'], y)
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
    t = QuerySet("http://foobar:9200", index="bar")
    wrapper = lambda y: map(lambda x: x['_id'], y)
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
    t.count().should.equal(1)


@httpretty.activate
def test_queryset_iteration_with_no_results():
    """
    Fetch results with QuerySet via __iter__ with no results
    """

    # When I create a query block
    t = QuerySet("http://foobar:9200", index="bar")
    wrapper = lambda y: map(lambda x: x['_id'], y)
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
    t = QuerySet("http://foobar:9200", index="bar")
    wrapper = lambda y: map(lambda x: x['_id'], y)
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
                           httpretty.Response(body=json.dumps(first_response)),
                           httpretty.Response(body=json.dumps(second_response)),
                        ],
                        content_type="application/json")

    # Then I should eventually get all records
    results = []
    for result in t:
        results.append(result)
    len(results).should.equal(3)
    t.count().should.equal(3)
    results[0].should.equal("1")
    results[1].should.equal("2")
    results[2].should.equal("3")

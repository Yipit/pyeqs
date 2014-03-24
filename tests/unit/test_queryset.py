# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Term, Sort, ScriptScore
from tests.helpers import compare


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

    compare(t._query, results)


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

    compare(t._query, results)


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

    compare(t._query, results)


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

    compare(t._query, results)


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

    compare(t._query, results)


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

    compare(t._query, results)


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

    compare(t._query, results)


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

    compare(t._query, results)

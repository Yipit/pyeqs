# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Term, Sort
from tests.helpers import compare


def test_create_queryset():
    """
    Create Default QuerySet
    """
    # When create a queryset
    t = QuerySet("http://foobar:9200")

    # Then I see the appropriate JSON
    results = {
        "query": { "match_all": {} }
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
                "query": { "match_all": {} },
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
                "query": { "match_all": {} },
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

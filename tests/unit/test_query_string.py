# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import QueryString
from tests.helpers import homogeneous


def test_query_string():
    """
    Create Query String Block
    """
    # When add create a query string
    t = QueryString("foo", fields=["bar"], use_dis_max=True, tie_breaker=0.05)

    # Then I see the appropriate JSON
    results = {
        "query_string": {
            "query": "foo",
            "fields": ["bar"],
            "tie_breaker": 0.05,
            "use_dis_max": True
        }
    }

    homogeneous(t, results)

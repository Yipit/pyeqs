# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httpretty
import json
import sure
from mock import Mock

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Term, Sort, ScriptScore
from tests.helpers import compare


def test_copy_queryset():
    """
    Copy Queryset object when used as Model
    """
    # When create a queryset
    t = QuerySet("http://foobar:9200")

    # And I query for results
    fake_response = {
        "hits": {
            "total": 2,
            "hits": ["foo", "bar"]
        }
    }

    connection = Mock()
    connection.search = Mock(return_value=fake_response)
    t._get_connection = Mock(return_value=connection)

    new_object = t.objects

    # Then the new object is not the same object as the queryset
    assert(new_object is not t)

    # And is not the same query object
    assert(new_object._query is not t._query)

    # But it is has the same properties
    assert(new_object._query.keys() == t._query.keys())

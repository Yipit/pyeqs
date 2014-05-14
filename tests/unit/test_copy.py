# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httpretty
import json
import sure
from mock import Mock

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Term, Sort, ScriptScore
from tests.helpers import heterogeneous, homogeneous


def test_copy_queryset():
    """
    Copy Queryset object when used as Model
    """
    # When create a queryset
    t = QuerySet("http://foobar:9200")

    new_object = t.objects

    # Then the new object is not the same object as the queryset
    assert(new_object is not t)

    # And is not the same query object
    assert(new_object._query is not t._query)

    # But it is has the same properties
    homogeneous(new_object._query, t._query)


def test_copy_queryset_with_filters():
    """
    Copy Queryset object and ensure distinct filters
    """
    # When create a queryset
    t = QuerySet("http://foobar:9200")

    # With filters
    t.filter(Term("foo", "bar"))

    # And I clone the queryset
    new_object = t.objects

    # And add new filters
    new_object.filter(Term("bar", "baz"))

    # Then the new object is not the same object as the queryset
    assert(new_object is not t)

    # And is not the same query object
    assert(new_object._query is not t._query)

    # But it is has the same properties
    heterogeneous(new_object._query, t._query)

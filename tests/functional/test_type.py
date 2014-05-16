# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Type
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_with_type(context):
    """
    Search with type filter
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3}, doc_type="bar")

    # And I add a type filter
    _type = Type("bar")
    t.filter(_type)
    results = t[0:10]

    # Then my results only have that type
    len(results).should.equal(1)
    results[0]["_source"]["bar"].should.equal(3)

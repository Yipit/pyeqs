# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import Exists
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_with_exists(context):
    """
    Search with exists filter
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"baz": 1})

    # And I add an exists filter
    exists = Exists("baz")
    t.filter(exists)
    results = t[0:10]

    # Then my results only have that field
    len(results).should.equal(1)
    results[0]["_source"]["baz"].should.equal(1)

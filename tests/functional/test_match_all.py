# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import MatchAll
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_match_all_search(context):
    """
    Search with match all filter
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz", "foo": "foo"})
    add_document("foo", {"bar": "baz", "foo": "foofoo"})
    add_document("foo", {"bar": "baz", "foo": "foofoofoo"})

    # And I filter match_all
    t.filter(MatchAll())
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(4)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Sort
from tests.helpers import compare

def test_add_sort():
    """
    Create Sort Block
    """
    # When add a Sort block
    t = Sort("foo", order="asc")

    # Then I see the appropriate JSON
    results = {
        "foo": {
            "order": "asc"
        }
    }

    compare(t, results)
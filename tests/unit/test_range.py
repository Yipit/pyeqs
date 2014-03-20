# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Range
from tests.helpers import compare

def test_add_range():
    """
    Create Range Block
    """
    # When add a Range Block
    t = Range("foo", gte="bar", lt="baz")

    # Then I see the appropriate JSON
    results = {
        "range": {
            "foo": {
                "gte": "bar",
                "lt": "baz"
            }
        }
    }

    compare(t, results)
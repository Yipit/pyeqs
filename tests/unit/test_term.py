# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Term
from tests.helpers import compare

def test_add_term():
    """
    Create Term Block
    """
    # When add a Term field
    t = Term("foo", "bar")

    # Then I see the appropriate JSON
    results = {
        "term": {
            "foo": "bar"
        }
    }

    compare(t, results)
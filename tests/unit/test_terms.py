# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Terms
from tests.helpers import homogeneous


def test_add_terms():
    """
    Create Terms Block
    """
    # When add a Terms field
    t = Terms("foo", ["bar", "baz"])

    # Then I see the appropriate JSON
    results = {
        "terms": {
            "foo": ["bar", "baz"]
        }
    }

    homogeneous(t, results)

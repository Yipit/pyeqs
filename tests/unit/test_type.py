# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Type
from tests.helpers import homogeneous


def test_add_type():
    """
    Create Type Block
    """
    # When add a Type Block
    t = Type("foo")

    # Then I see the appropriate JSON
    results = {
        "type": {
            "value": "foo"
        }
    }

    homogeneous(t, results)

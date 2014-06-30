# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Exists
from tests.helpers import homogeneous


def test_exists():
    """
    Create Exists Block
    """
    # When add an Exists Block
    t = Exists("foo")

    # Then I see the appropriate JSON
    results = {
        "exists": {
            "field": "foo"
        }
    }

    homogeneous(t, results)

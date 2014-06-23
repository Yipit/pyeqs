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


def test_add_terms_with_execution():
    """
    Create Terms With Execution
    """
    # When add a Terms field
    t = Terms("foo", ["bar", "baz"], execution="and")

    # Then I see the appropriate JSON
    results = {
        "terms": {
            "foo": ["bar", "baz"],
            "execution": "and"

        }
    }

    homogeneous(t, results)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Missing
from tests.helpers import homogeneous


def test_missing():
    """
    Create Missing Block
    """
    # When add a Missing Block
    t = Missing("foo")

    # Then I see the appropriate JSON
    results = {
        "missing": {
            "field": "foo"
        }
    }

    homogeneous(t, results)


def test_missing_existence():
    """
    Create Missing Block with Existence
    """
    # When add a Missing Block
    t = Missing("foo", existence=True)

    # Then I see the appropriate JSON
    results = {
        "missing": {
            "field": "foo",
            "existence": True
        }
    }

    homogeneous(t, results)


def test_missing_null_value():
    """
    Create Missing Block with Null Value
    """
    # When add a Missing Block
    t = Missing("foo", null_value=True)

    # Then I see the appropriate JSON
    results = {
        "missing": {
            "field": "foo",
            "null_value": True
        }
    }

    homogeneous(t, results)

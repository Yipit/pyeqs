# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Sort
from tests.helpers import compare


def test_add_sort():
    """
    Create Sort Block
    """
    # When add a Sort block
    t = Sort("foo")

    # Then I see the appropriate JSON
    results = {
        "foo": {
            "order": "asc"
        }
    }

    compare(t, results)


def test_add_sort_asc():
    """
    Create Sort Block Ascending
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


def test_add_sort_desc():
    """
    Create Sort Block Descending
    """
    # When add a Sort block
    t = Sort("foo", order="dsc")

    # Then I see the appropriate JSON
    results = {
        "foo": {
            "order": "dsc"
        }
    }

    compare(t, results)


def test_add_sort_with_mode():
    """
    Create Sort Block with Mode
    """
    # When add a Sort block
    t = Sort("foo", mode="bar")

    # Then I see the appropriate JSON
    results = {
        "foo": {
            "order": "asc",
            "mode": "bar"
        }
    }

    compare(t, results)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Range
from tests.helpers import compare


def test_add_gte_range():
    """
    Create Greater Than Or Equal Range Block
    """
    # When add a Range Block
    t = Range("foo", gte="bar")

    # Then I see the appropriate JSON
    results = {
        "range": {
            "foo": {
                "gte": "bar",
            }
        }
    }

    compare(t, results)


def test_add_gt_range():
    """
    Create Greater Than Range Block
    """
    # When add a Range Block
    t = Range("foo", gt="bar")

    # Then I see the appropriate JSON
    results = {
        "range": {
            "foo": {
                "gt": "bar"
            }
        }
    }

    compare(t, results)


def test_add_lte_range():
    """
    Create Less Than Or Equal Range Block
    """
    # When add a Range Block
    t = Range("foo", lte="bar")

    # Then I see the appropriate JSON
    results = {
        "range": {
            "foo": {
                "lte": "bar"
            }
        }
    }

    compare(t, results)


def test_add_lt_range():
    """
    Create Less Than Range Block
    """
    # When add a Range Block
    t = Range("foo", lt="bar")

    # Then I see the appropriate JSON
    results = {
        "range": {
            "foo": {
                "lt": "bar"
            }
        }
    }

    compare(t, results)

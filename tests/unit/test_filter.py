# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs import Filter
from pyeqs.dsl import Term
from tests.helpers import homogeneous


def test_create_filter():
    """
    Create Default Filter
    """
    # When create a filter block
    t = Filter()

    # Then I see the appropriate JSON
    results = {
        "and": []
    }

    homogeneous(t, results)


def test_add_filter():
    """
    Create Filter with Block
    """
    # When I create a filter
    t = Filter()

    # And add a block
    t.filter(Term("foo", "bar"))

    # Then I see the appropriate JSON
    results = {
        "and": [
            {
                "term": {
                    "foo": "bar"
                }
            }
        ]
    }

    homogeneous(t, results)


def test_filter_with_or():
    """
    Create OR Filter
    """
    # When create a filter block
    t = Filter("or")

    # Then I see the appropriate JSON
    results = {
        "or": []
    }

    homogeneous(t, results)


def test_filter_with_and():
    """
    Create AND Filter
    """
    # When create a filter block
    t = Filter("and")

    # Then I see the appropriate JSON
    results = {
        "and": []
    }

    homogeneous(t, results)

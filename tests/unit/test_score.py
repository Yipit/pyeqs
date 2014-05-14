# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import ScriptScore
from tests.helpers import homogeneous


def test_add_score():
    """
    Create Score Block
    """
    # When add a Score field
    t = ScriptScore("foo")

    # Then I see the appropriate JSON
    results = {
        "script": "foo"
    }

    homogeneous(t, results)


def test_add_score_with_params():
    """
    Create Score Block with Params
    """
    # When add a Score field
    t = ScriptScore("foo", params={"bar": "baz"})

    # Then I see the appropriate JSON
    results = {
        "script": "foo",
        "params": {
            "bar": "baz"
        }
    }

    homogeneous(t, results)


def test_add_score_with_lang():
    """
    Create Score Block with Language
    """
    # When add a Score field
    t = ScriptScore("foo", lang="mvel")

    # Then I see the appropriate JSON
    results = {
        "script": "foo",
        "lang": "mvel"
    }

    homogeneous(t, results)


def test_add_score_with_params_and_lang():
    """
    Create Score Block with Params and Language
    """
    # When add a Score field
    t = ScriptScore("foo", params={"bar": "baz"}, lang="mvel")

    # Then I see the appropriate JSON
    results = {
        "script": "foo",
        "params": {
            "bar": "baz"
        },
        "lang": "mvel"
    }

    homogeneous(t, results)

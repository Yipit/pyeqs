# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs import Bool
from pyeqs.dsl import Term
from tests.helpers import homogeneous


def test_create_bool():
    """
    Create Bool Block
    """
    # When I create a Bool block
    t = Bool()

    # Then I see the appropriate JSON
    results = {
        "bool": {}
    }

    homogeneous(t, results)


def test_create_bool_with_must():
    """
    Create Bool Block with Must
    """
    # When I create a Bool block
    t = Bool()

    # And add a 'must' condition with a Term
    t.must(Term("foo", "bar"))

    # Then I see the appropriate JSON
    results = {
        "bool": {
            "must": [
                {
                    "term": {
                        "foo": "bar"
                    }
                }
            ]
        }
    }

    homogeneous(t, results)


def test_create_bool_with_must_not():
    """
    Create Bool Block with Must Not
    """
    # When I create a Bool block
    t = Bool()

    # And add a 'must_not' condition with a Term
    t.must_not(Term("foo", "bar"))

    # Then I see the appropriate JSON
    results = {
        "bool": {
            "must_not": [
                {
                    "term": {
                        "foo": "bar"
                    }
                }
            ]
        }
    }

    homogeneous(t, results)


def test_create_bool_with_should():
    """
    Create Bool Block with Should
    """
    # When I create a Bool block
    t = Bool()

    # And add a 'should' condition with a Term
    t.should(Term("foo", "bar"))

    # Then I see the appropriate JSON
    results = {
        "bool": {
            "should": [
                {
                    "term": {
                        "foo": "bar"
                    }
                }
            ]
        }
    }

    homogeneous(t, results)


def test_create_bool_with_multiple_clauses():
    """
    Create Bool Block with Multiple Clauses
    """
    # When I create a Bool block
    t = Bool()

    # And add multiple conditions
    t.must_not(Term("foo", "foo"))\
     .must(Term("bar", "bar"))\
     .should(Term("baz", "baz"))\
     .should(Term("foobar", "foobar"))

    # Then I see the appropriate JSON
    results = {
        "bool": {
            "must_not": [
                {
                    "term": {
                        "foo": "foo"
                    }
                }
            ],
            "must": [
                {
                    "term": {
                        "bar": "bar"
                    }
                }
            ],
            "should": [
                {
                    "term": {
                        "baz": "baz"
                    }
                },
                {
                    "term": {
                        "foobar": "foobar"
                    }
                },
            ]
        }
    }

    homogeneous(t, results)

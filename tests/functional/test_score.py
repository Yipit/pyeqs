# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import ScriptScore, Exists
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_with_scoring(context):
    """
    Search with custom scoring
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add scoring
    score = ScriptScore("s = 0 + doc['bar'].value")
    t.score(score)
    results = t[0:10]

    # Then my results are scored correctly
    len(results).should.equal(3)
    results[0]["_source"]["bar"].should.equal(3)
    results[1]["_source"]["bar"].should.equal(2)
    results[2]["_source"]["bar"].should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_search_with_scoring_and_lang(context):
    """
    Search with custom scoring and language
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add scoring with a language
    score = ScriptScore("s = 0 + doc['bar'].value", lang="mvel")
    t.score(score)
    results = t[0:10]

    # Then my results are scored correctly
    len(results).should.equal(3)
    results[0]["_source"]["bar"].should.equal(3)
    results[1]["_source"]["bar"].should.equal(2)
    results[2]["_source"]["bar"].should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_search_with_scoring_and_params(context):
    """
    Search with custom scoring and params
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3})

    # And I add scoring with params
    score = ScriptScore("s = custom_param + doc['bar'].value", params={"custom_param": 1})
    t.score(score)
    results = t[0:10]

    # Then my results are scored correctly
    len(results).should.equal(3)
    results[0]["_source"]["bar"].should.equal(3)
    results[1]["_source"]["bar"].should.equal(2)
    results[2]["_source"]["bar"].should.equal(1)


@scenario(prepare_data, cleanup_data)
def test_search_multiple_scoring(context):
    """
    Search with custom scoring and params
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1, "baz": 4})
    add_document("foo", {"bar": 1})

    # And I add scoring with params
    score = ScriptScore("s = custom_param + doc['bar'].value", params={"custom_param": 1})
    t.score(score)

    boost = {
        "boost_factor": "10",
        "filter": Exists("baz")
    }
    t.score(boost)
    results = t[0:10]

    # Then my results are scored correctly
    len(results).should.equal(2)
    results[0]["_source"]["baz"].should.equal(4)
    ("baz" in results[1]["_source"].keys()).should.be.false

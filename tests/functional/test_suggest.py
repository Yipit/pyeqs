# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet
from pyeqs.dsl import TermSuggesters
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_term_suggest(context):
    """
    Search with term suggest
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "bazzab", "fizz": "buzzbee"})
    add_document("foo", {"bar": "bazzab", "fizz": "buzzbee"})
    add_document("foo", {"bar": "bazbaz", "fizz": "buzzbee"})
    add_document("foo", {"bar": "bazbaz", "fizz": "buzzbet"})
    add_document("foo", {"bar": "bazbaz", "fizz": "buzzbat"})
    add_document("foo", {"bar": "barbaz", "fizz": "buzzbuz"})
    add_document("foo", {"bar": "barbaz", "fizz": "buzzboe"})
    add_document("foo", {"bar": "foobar", "fizz": "buzzboe"})

    # And I do a suggest search
    t.suggest(suggestion=TermSuggesters("spelling", "bazbat", "bar"))
    t[0:10]

    # Then I get the the expected results
    t.suggestions().should.have.key("spelling")
    t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbat")
    t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
    t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
    t.suggestions()["spelling"][0].should.have.key("options")
    t.suggestions()["spelling"][0]["options"].should.be.equal([
        {u'text': u'bazbaz', u'freq': 3, u'score': 0.8333333},
        {u'text': u'barbaz', u'freq': 2, u'score': 0.6666666},
        {u'text': u'bazzab', u'freq': 2, u'score': 0.6666666}])

    # If I do it again
    t.suggest(suggestion=TermSuggesters("not_spelling", "buzzbie", "fizz"))
    t[0:10]

    # Then I get the the expected results
    t.suggestions().should.have.key("not_spelling")
    t.suggestions()["not_spelling"][0].should.have.key("text").being.equal("buzzbie")
    t.suggestions()["not_spelling"][0].should.have.key("length").being.equal(7)
    t.suggestions()["not_spelling"][0].should.have.key("offset").being.equal(0)
    t.suggestions()["not_spelling"][0].should.have.key("options")
    t.suggestions()["not_spelling"][0]["options"].should.be.equal([
        {u'text': u'buzzbee', u'freq': 3, u'score': 0.85714287},
        {u'text': u'buzzboe', u'freq': 2, u'score': 0.85714287},
        {u'text': u'buzzbat', u'freq': 1, u'score': 0.71428573},
        {u'text': u'buzzbet', u'freq': 1, u'score': 0.71428573},
        {u'text': u'buzzbuz', u'freq': 1, u'score': 0.71428573}])


@scenario(prepare_data, cleanup_data)
def test_search_global_term_suggest(context):
    """
    Search with global term suggest
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "barbaz"})
    add_document("foo", {"bar": "barbaz"})
    add_document("foo", {"bar": "foobar"})

    # And I do a suggest search
    t.suggest(suggestion=TermSuggesters("spelling", "bazbat", "bar", global_=True))
    t[0:10]

    # Then I get the the expected results
    t.suggestions().should.have.key("spelling")
    t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbat")
    t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
    t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
    t.suggestions()["spelling"][0].should.have.key("options")
    t.suggestions()["spelling"][0]["options"].should.be.equal([
        {u'text': u'bazbaz', u'freq': 3, u'score': 0.8333333},
        {u'text': u'barbaz', u'freq': 2, u'score': 0.6666666},
        {u'text': u'bazzab', u'freq': 2, u'score': 0.6666666}])


@scenario(prepare_data, cleanup_data)
def test_search_term_suggest_with_size(context):
    """
    Search with term suggest w/ specified size
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "barbaz"})
    add_document("foo", {"bar": "foobar"})

    # And I do a suggest search
    t.suggest(suggestion=TermSuggesters("spelling", "bazbat", "bar", size=2))
    t[0:10]

    # Then I get the the expected results
    t.suggestions().should.have.key("spelling")
    t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbat")
    t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
    t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
    t.suggestions()["spelling"][0].should.have.key("options")
    t.suggestions()["spelling"][0]["options"].should.be.equal([
        {u'text': u'bazbaz', u'freq': 3, u'score': 0.8333333},
        {u'text': u'bazzab', u'freq': 2, u'score': 0.6666666}])


@scenario(prepare_data, cleanup_data)
def test_search_term_suggest_with_sort(context):
    """
    Search with term suggest w/ sort
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "barbaz"})
    add_document("foo", {"bar": "foobar"})

    # And I do a suggest search
    t.suggest(suggestion=TermSuggesters("spelling", "barbat", "bar", sort="frequency"))
    t[0:10]

    # Then I get the the expected results
    t.suggestions().should.have.key("spelling")
    t.suggestions()["spelling"][0].should.have.key("text").being.equal("barbat")
    t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
    t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
    t.suggestions()["spelling"][0].should.have.key("options")
    t.suggestions()["spelling"][0]["options"].should.be.equal([
        {u'text': u'bazbaz', u'freq': 3, u'score': 0.6666666},
        {u'text': u'barbaz', u'freq': 1, u'score': 0.8333333}])


@scenario(prepare_data, cleanup_data)
def test_search_term_suggest_with_suggest_mode(context):
    """
    Search with term suggest w/ suggest_mode
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "barbaz"})
    add_document("foo", {"bar": "foobar"})

    # And I do a suggest search
    t.suggest(suggestion=TermSuggesters("spelling", "bazbat", "bar", suggest_mode="popular"))
    t[0:10]

    # Then I get the the expected results
    t.suggestions().should.have.key("spelling")
    t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbat")
    t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
    t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
    t.suggestions()["spelling"][0].should.have.key("options")
    t.suggestions()["spelling"][0]["options"].should.be.equal([
        {u'text': u'bazbaz', u'freq': 3, u'score': 0.8333333},
        {u'text': u'bazzab', u'freq': 2, u'score': 0.6666666},
        {u'text': u'barbaz', u'freq': 1, u'score': 0.6666666}])


@scenario(prepare_data, cleanup_data)
def test_search_term_suggest_with_max_edits(context):
    """
    Search with term suggest w/ max_edits
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "barbaz"})
    add_document("foo", {"bar": "foobar"})

    # And I do a suggest search (can be either 1 or 2, defaults to 2)
    t.suggest(suggestion=TermSuggesters("spelling", "bazbat", "bar", max_edits=1))
    t[0:10]

    # Then I get the the expected results
    t.suggestions().should.have.key("spelling")
    t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbat")
    t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
    t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
    t.suggestions()["spelling"][0].should.have.key("options")
    t.suggestions()["spelling"][0]["options"].should.be.equal([
        {u'text': u'bazbaz', u'freq': 3, u'score': 0.8333333}])


@scenario(prepare_data, cleanup_data)
def test_search_term_suggest_with_prefix_length(context):
    """
    Search with term suggest w/ prefix_length
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazzab"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "barbaz"})
    add_document("foo", {"bar": "foobar"})

    # And I do a suggest search
    t.suggest(suggestion=TermSuggesters("spelling", "bazbat", "bar", prefix_length=3))
    t[0:10]

    # Then I get the the expected results
    t.suggestions().should.have.key("spelling")
    t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbat")
    t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
    t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
    t.suggestions()["spelling"][0].should.have.key("options")
    t.suggestions()["spelling"][0]["options"].should.be.equal([
        {u'text': u'bazbaz', u'freq': 3, u'score': 0.8333333},
        {u'text': u'bazzab', u'freq': 2, u'score': 0.6666666}])


# @scenario(prepare_data, cleanup_data)
# def test_search_term_suggest_with_min_word_length(context):
#     """
#     Search with term suggest w/ specified min_word_length
#     """
#     # When create a queryset
#     t = QuerySet("localhost", index="foo")

#     # And there are records
#     add_document("foo", {"bar": "bazzabzxcvxc"})
#     add_document("foo", {"bar": "bazzabzxcvxc"})
#     add_document("foo", {"bar": "bazbazzxcvx"})
#     add_document("foo", {"bar": "bazbazzxcvx"})
#     add_document("foo", {"bar": "bazbaz"})
#     add_document("foo", {"bar": "barbaz"})
#     add_document("foo", {"bar": "foobar"})

#     # And I do a suggest search
#     t.suggest(suggestion=TermSuggesters("spelling", "bazbazzxcvxc", "bar", min_word_length=12))
#     t[0:10]

#     # Then I get the the expected results
#     t.suggestions().should.have.key("spelling")
#     t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbazzxcvxc")
#     t.suggestions()["spelling"][0].should.have.key("length").being.equal(12)
#     t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
#     t.suggestions()["spelling"][0].should.have.key("options")
#     t.suggestions()["spelling"][0]["options"].should.be.equal([
#         {u'text': u'bazzabzxcvxc', u'freq': 2, u'score': 0.8333333}])


# @scenario(prepare_data, cleanup_data)
# def test_search_term_suggest_with_min_doc_freq(context):
#     """
#     Search with term suggest w/ min_doc_freq
#     """
#     # When create a queryset
#     t = QuerySet("localhost", index="foo")

#     # And there are enough records per shard
#     add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"})
#     add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"}), add_document("foo", {"bar": "bazzab"})
#     add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"})
#     add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"})
#     add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"}), add_document("foo", {"bar": "bazbaz"})
#     add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"})
#     add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"}), add_document("foo", {"bar": "barbaz"})
#     add_document("foo", {"bar": "foobar"}), add_document("foo", {"bar": "foobar"}), add_document("foo", {"bar": "foobar"}), add_document("foo", {"bar": "foobar"}), add_document("foo", {"bar": "foobar"}), add_document("foo", {"bar": "foobar"}), add_document("foo", {"bar": "foobar"})

#     # And I do a suggest search
#     t.suggest(suggestion=TermSuggesters("spelling", "bazbat", "bar", min_doc_freq=5))
#     t[0:10]

#     # Then I get the the expected results
#     t.suggestions().should.have.key("spelling")
#     t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbat")
#     t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
#     t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
#     t.suggestions()["spelling"][0].should.have.key("options")
#     t.suggestions()["spelling"][0]["options"].should.be.equal([
#         {u'text': u'bazbaz', u'freq': 6, u'score': 0.8333333}])


# @scenario(prepare_data, cleanup_data)
# def test_search_term_suggest_with_max_term_freq(context):
#     """
#     Search with term suggest w/ max_term_freq
#     """
#     # When create a queryset
#     t = QuerySet("localhost", index="foo")

#     # And there are enough records per shard
#     add_document("foo", {"bar": "bazzab"})
#     add_document("foo", {"bar": "bazzab"})
#     add_document("foo", {"bar": "bazbaz"})
#     add_document("foo", {"bar": "bazbaz"})
#     add_document("foo", {"bar": "bazbaz"})
#     add_document("foo", {"bar": "barbaz"})
#     add_document("foo", {"bar": "barbaz"})
#     add_document("foo", {"bar": "foobar"})

#     # And I do a suggest search
#     t.suggest(suggestion=TermSuggesters("spelling", "bazbat", "bar", max_term_freq=0.1))
#     t[0:10]

#     # Then I get the the expected results
#     t.suggestions().should.have.key("spelling")
#     t.suggestions()["spelling"][0].should.have.key("text").being.equal("bazbat")
#     t.suggestions()["spelling"][0].should.have.key("length").being.equal(6)
#     t.suggestions()["spelling"][0].should.have.key("offset").being.equal(0)
#     t.suggestions()["spelling"][0].should.have.key("options")
#     t.suggestions()["spelling"][0]["options"].should.be.equal([
#         {u'text': u'bazbaz', u'freq': 3, u'score': 0.8333333},
#         {u'text': u'bazzab', u'freq': 2, u'score': 0.6666666},
#         {u'text': u'barbaz', u'freq': 2, u'score': 0.6666666}])

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from pyeqs.dsl import TermSuggesters


def test_add_term_suggest():
    """
    Create a term suggest block
    """
    # When I add a term suggest block
    t = TermSuggesters("sugg_name", "text_content", "field_name")

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_with_size():
    """
    Create a term suggest block w/ specified size
    """
    # When I add a term suggest block
    t = TermSuggesters("sugg_name", "text_content", "field_name", size=7)

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 0.01,
                "size": 7
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_global_term():
    """
    Create a global term suggest block
    """
    # When I add a term suggest block
    t = TermSuggesters("sugg_name", "text_content", "field_name", global_=True)

    # Then I see the correct json
    results = {
        "text": "text_content",
        "sugg_name": {
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_with_sort():
    """
    Create a term suggest block w/ frequency sort
    """
    # When I add a term suggest block
    t = TermSuggesters("sugg_name", "text_content", "field_name", sort="frequency")

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "frequency",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_with_suggest_mode():
    """
    Create a term suggest block w/ specified suggest_mode
    """
    # When I add a term suggest block
    t = TermSuggesters("sugg_name", "text_content", "field_name", suggest_mode="popular")

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "popular",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_with_max_edits():
    """
    Create a term suggest block w/ specified max_edits
    """
    # When I add a term suggest block with 1 instead of default 2
    t = TermSuggesters("sugg_name", "text_content", "field_name", max_edits=1)

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 1,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_with_prefix_length():
    """
    Create a term suggest block w/ specified prefix_length
    """
    # When I add a term suggest block
    t = TermSuggesters("sugg_name", "text_content", "field_name", prefix_length=7)

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 7,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_with_min_word_length():
    """
    Create a term suggest block w/ specified min_word_length
    """
    # When I add a term suggest block
    t = TermSuggesters("sugg_name", "text_content", "field_name", min_word_length=7)

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 7,
                "min_doc_freq": 0,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_with_min_doc_freq():
    """
    Create a term suggest block w/ specified min_doc_freq
    """
    # When I add a term suggest block with an absolute number
    t = TermSuggesters("sugg_name", "text_content", "field_name", min_doc_freq=7)

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 7,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))

    # When I add a term suggest block with a relative percentage of number of docs
    t = TermSuggesters("sugg_name", "text_content", "field_name", min_doc_freq=0.39)

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0.39,
                "max_term_freq": 0.01
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))


def test_add_term_suggest_with_max_term_freq():
    """
    Create a term suggest block w/ specified max_term_freq
    """
    # When I add a term suggest block with an absolute number
    t = TermSuggesters("sugg_name", "text_content", "field_name", max_term_freq=7)

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 7
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))

    # When I add a term suggest block with a relative percentage number of docs
    t = TermSuggesters("sugg_name", "text_content", "field_name", max_term_freq=0.39)

    # Then I see the correct json
    results = {
        "sugg_name": {
            "text": "text_content",
            "term": {
                "field": "field_name",
                "sort": "score",
                "suggest_mode": "missing",
                "max_edits": 2,
                "prefix_length": 1,
                "min_word_length": 4,
                "min_doc_freq": 0,
                "max_term_freq": 0.39
            }
        }
    }

    json.dumps(t).should.equal(json.dumps(results))

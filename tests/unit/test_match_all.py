# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import MatchAll
from tests.helpers import homogeneous


def test_add_match_all():
    """
    Create Match All Block
    """
    # When add a match all filter
    t = MatchAll()

    # Then I see the appropriate JSON
    results = {
        "match_all": {}
    }

    homogeneous(t, results)

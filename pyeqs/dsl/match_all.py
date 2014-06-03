# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class MatchAll(dict):

    def __init__(self):
        super(MatchAll, self).__init__()
        self._build_dict()

    def _build_dict(self):
        self["match_all"] = {}

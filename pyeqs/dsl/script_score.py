# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class ScriptScore(dict):

    def __init__(self, script, params=None, lang=None):
        super(ScriptScore, self).__init__()
        self.script = script
        self.params = params
        self.lang = lang
        self._build_dict()

    def _build_dict(self):
        self["script"] = self.script
        if self.params:
            self["params"] = self.params
        if self.lang:
            self["lang"] = self.lang

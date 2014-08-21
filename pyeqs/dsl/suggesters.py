# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class TermSuggesters(dict):

    def __init__(self, sugg_name, text, field_name, global_=False, size=None,
                 sort="score", suggest_mode="missing", max_edits=2, prefix_length=1,
                 min_word_length=4, min_doc_freq=0, max_term_freq=0.01):
        super(TermSuggesters, self).__init__()
        self.sugg_name = sugg_name
        self.text = text
        self.field_name = field_name
        self._global = global_
        self.size = size
        self.sort = sort
        self.suggest_mode = suggest_mode
        self.max_edits = max_edits
        self.prefix_length = prefix_length
        self.min_word_length = min_word_length
        self.min_doc_freq = min_doc_freq
        self.max_term_freq = max_term_freq
        self._build_dict()

    def _build_dict(self):
        self[self.sugg_name] = {"term": {
            "field": self.field_name,
            "sort": self.sort,
            "suggest_mode": self.suggest_mode,
            "max_edits": self.max_edits,
            "prefix_length": self.prefix_length,
            "min_word_length": self.min_word_length,
            "min_doc_freq": self.min_doc_freq,
            "max_term_freq": self.max_term_freq
        }}

        if self._global:
            self.update({"text": self.text})
        else:
            self[self.sugg_name].update({"text": self.text})

        if self.size:
            self[self.sugg_name]["term"].update({"size": self.size})

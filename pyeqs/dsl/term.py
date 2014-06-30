# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Term(dict):

    def __init__(self, field_name, term):
        super(Term, self).__init__()
        self.field_name = field_name
        self.term = term
        self["term"] = self._build_dict()

    def _build_dict(self):
        return {
            self.field_name: self.term
        }

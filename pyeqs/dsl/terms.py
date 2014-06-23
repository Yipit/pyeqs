# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Terms(dict):

    def __init__(self, field_name, terms, execution=None):
        super(Terms, self).__init__()
        self.field_name = field_name
        self.terms = terms
        self.execution = execution
        self["terms"] = self._build_dict()

    def _build_dict(self):
        terms = {
            self.field_name: self.terms
        }
        if self.execution is not None:
            terms["execution"] = self.execution
        return terms

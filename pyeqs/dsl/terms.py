# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

class Terms(dict):

    def __init__(self, field_name, terms):
        super(Terms, self).__init__()
        self.field_name = field_name
        self.terms = terms
        self["terms"] = self._build_dict()

    def _build_dict(self):
        return {
            self.field_name: self.terms
        }
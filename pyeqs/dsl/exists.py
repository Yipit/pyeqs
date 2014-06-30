# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Exists(dict):

    def __init__(self, field):
        super(Exists, self).__init__()
        self.field = field
        self["exists"] = self._build_dict()

    def _build_dict(self):
        return {
            "field": self.field
        }

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

class Sort(dict):

    def __init__(self, field, order="asc", mode=None):
        super(Sort, self).__init__()
        self.field = field
        self.order = order
        self.mode = mode
        self._build_dict()

    def _build_dict(self):
        sorting = {}
        sorting["order"] = self.order
        if self.mode:
            sorting["mode"] = self.mode
        self[self.field] = sorting
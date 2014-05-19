# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Range(dict):

    def __init__(self, field_name, gte=None, gt=None, lte=None, lt=None):
        super(Range, self).__init__()
        self.field_name = field_name
        self.gte = gte
        self.gt = gt
        self.lte = lte
        self.lt = lt
        self["range"] = self._build_dict()

    def _build_dict(self):
        _range = {
                self.field_name: {}
            }
        if self.gte:
            _range[self.field_name]["gte"] = self.gte
        if self.gt:
            _range[self.field_name]["gt"] = self.gt
        if self.lte:
            _range[self.field_name]["lte"] = self.lte
        if self.lt:
            _range[self.field_name]["lt"] = self.lt
        return _range

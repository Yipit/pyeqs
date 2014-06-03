# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Missing(dict):

    def __init__(self, field, existence=None, null_value=None):
        super(Missing, self).__init__()
        self.field = field
        self.existence = existence
        self.null_value = null_value
        self["missing"] = self._build_dict()

    def _build_dict(self):
        missing = {"field": self.field}
        if self.existence is not None:
            missing["existence"] = self.existence
        if self.null_value is not None:
            missing["null_value"] = self.null_value
        return missing

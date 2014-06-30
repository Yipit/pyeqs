# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Type(dict):

    def __init__(self, type_name):
        super(Type, self).__init__()
        self.type_name = type_name
        self["type"] = self._build_dict()

    def _build_dict(self):
        return {
            "value": self.type_name
        }

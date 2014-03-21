# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Filter(dict):

    def __init__(self, operator="and"):
        super(Filter, self).__init__()
        self.operator = operator
        self[self.operator] = []

    def filter(self, new_filter):
        self[self.operator].append(new_filter)
        return self

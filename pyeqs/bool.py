# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Bool(dict):

    def __init__(self):
        super(Bool, self).__init__()
        self.must = []
        self.must_not = []
        self.should = []
        self["bool"] = {}

    def bool(self, must=None, must_not=None, should=None):
        if must:
            self.must.append(must)
            self["bool"]["must"] = self.must
        if must_not:
            self.must_not.append(must_not)
            self["bool"]["must_not"] = self.must_not
        if should:
            self.should.append(should)
            self["bool"]["should"] = self.should
        return self

    def must(self, block):
        return self.bool(must=block)

    def must_not(self, block):
        return self.bool(must_not=block)

    def should(self, block):
        return self.bool(should=block)

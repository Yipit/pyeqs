# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class QueryString(dict):

    def __init__(self, query, fields=None, tie_breaker=None, use_dis_max=None):
        super(QueryString, self).__init__()
        self.query = query
        self.fields = fields
        self.tie_breaker = tie_breaker
        self.use_dis_max = use_dis_max
        self["query_string"] = self._build_dict()

    def _build_dict(self):
        query_string = {"query": self.query}
        if self.fields is not None:
            query_string["fields"] = self.fields
        if self.use_dis_max is not None:
            query_string["use_dis_max"] = self.use_dis_max
        if self.tie_breaker is not None:
            query_string["tie_breaker"] = self.tie_breaker
        return query_string

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import copy

from pyelasticsearch import ElasticSearch
from . import Filter, Bool


class QuerySet(object):

    def __init__(self, host, query=None, index='', ):
        self._host = host
        self._index = index
        self._query = {"query": {}}
        self._query_string = query
        self._query_formed = False
        self._filtered = False
        self._scored = False
        self._sorted = False
        self._wrappers = []
        self._count = 0
        self._conn = None
        self._build_query()

    def filter(self, f, operator="and"):
        if self._filtered:
            if self._scored:
                self._query["query"]["function_score"]["query"]["filtered"]["filter"].filter(f)
            else:
                self._query["query"]["filtered"]["filter"].filter(f)
        else:
            self._build_filtered_query()
            if isinstance(f, Filter):
                if self._scored:
                    self._query["query"]["function_score"]["query"]["filtered"]["filter"] = f
                else:
                    self._query["query"]["filtered"]["filter"] = f
            else:
                if self._scored:
                    self._query["query"]["function_score"]["query"]["filtered"]["filter"] = Filter(operator).filter(f)
                else:
                    self._query["query"]["filtered"]["filter"] = Filter(operator).filter(f)
        return self

    def score(self, script_score, boost_mode="replace"):
        if not self._scored:
            self._build_scored_query()
        self._query["query"]["function_score"]["script_score"] = script_score
        self._query["query"]["function_score"]["boost_mode"] = boost_mode
        return self

    def only(self, fields):
        self._query["fields"] = fields
        return self

    def order_by(self, sorting):
        if not self._sorted:
            self._build_sorted_query()
        self._query["sort"].append(sorting)
        return self

    def wrappers(self, wrapper):
        self._wrappers.append(wrapper)
        return self

    def count(self):
        return self._count

    def _build_query(self):
        if self._query_string:
            self._query["query"] = {
                "query_string": {
                    "query": self._query_string
                }
            }
        else:
            self._query["query"] = {
                "match_all": {}
            }

    def _build_filtered_query(self):
        self._filtered = True
        if self._scored:
            q = copy.deepcopy(self._query["query"]["function_score"]["query"])
        else:
            q = copy.deepcopy(self._query["query"])
        filtered_query = {
            "filtered": {
                "filter": {},
                "query": q
            }
        }
        if self._scored:
            self._query["query"]["function_score"]["query"] = filtered_query
        else:
            self._query["query"] = filtered_query

    def _build_scored_query(self):
        self._scored = True
        q = copy.deepcopy(self._query["query"])
        self._query["query"] = {
            "function_score": {
                "query": q
            }
        }

    def _build_sorted_query(self):
        self._sorted = True
        self._query["sort"] = []

    def __getitem__(self, val):
        """
        Override __getitem__ so we can activate our ES call when we try to slice
        """
        start = val.start
        end = val.stop
        results = self._search(start, end)
        for wrapper in self._wrappers:
            results = wrapper(results)
        return results

    def _search(self, start, end):
        conn = self._get_connection()
        pagination_kwargs = self._get_pagination_kwargs(start, end)
        self._raw_results = conn.search(self._query, index=self._index, **pagination_kwargs)
        self._count = self._get_result_count(self._raw_results)
        return self._raw_results["hits"]["hits"]

    def _get_result_count(self, results):
        return int(results["hits"]["total"])

    def _get_pagination_kwargs(self, start, end):
        size = end - start
        kwargs = {
            'es_from': start,
            'es_size': size
        }
        return kwargs

    def _get_connection(self):
        if not self._conn:
            self._conn = ElasticSearch(self._host)
        return self._conn

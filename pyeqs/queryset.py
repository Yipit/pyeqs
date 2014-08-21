# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from copy import deepcopy

from elasticsearch import Elasticsearch
from six import string_types
from . import QueryBuilder


class QuerySet(object):

    def __init__(self, host, query=None, index=''):
        self._host = host
        self._index = index
        if isinstance(query, QueryBuilder):
            self._q = query
        else:
            self._q = QueryBuilder(query_string=query)
        self._wrappers = []
        self._post_query_actions = []
        self._count = None
        self._max_score = None
        self._conn = None
        self._finalized_query = None
        self._aggregations = None
        # Caching
        self._cache = None
        self._retrieved = 0
        self._per_request = 10

    def _clone(self):
        klass = self.__class__
        query = deepcopy(self._q)
        clone = klass(self._host, query=query, index=self._index)
        clone._conn = self._conn
        return clone

    @property
    def objects(self):
        return self._clone()

    @property
    def _query(self):
        return self._q._finalize_query()

    def filter(self, f, operator="and"):
        self._q.filter(f, operator=operator)
        return self

    def score(self, scoring_block, boost_mode="replace", score_mode="multiply", min_score=None, track_scores=False):
        self._q.score(scoring_block, boost_mode=boost_mode, score_mode=score_mode, min_score=min_score, track_scores=track_scores)
        return self

    def only(self, fields):
        self._q.fields(fields)
        return self

    def order_by(self, sorting):
        self._q.sort(sorting)
        return self

    def wrappers(self, wrapper):
        self._wrappers.append(wrapper)
        return self

    def post_query_actions(self, action):
        self._post_query_actions.append(action)
        return self

    def count(self):
        return self._count

    def max_score(self):
        return self._max_score

    def aggregations(self):
        return self._aggregations

    def aggregate(self, aggregation):
        self._q.aggregate(aggregation)
        return self

    def __next__(self):
        return self.next()  # pragma: no cover

    def next(self):
        """
        Provide iteration capabilities

        Use a small object cache for performance
        """
        if not self._cache:
            self._cache = self._get_results()
            self._retrieved += len(self._cache)

        # If we don't have any other data to return, we just
        # stop the iteration.
        if not self._cache:
            raise StopIteration()

        # Consuming the cache and updating the "cursor"
        return self._cache.pop(0)

    def _get_results(self):
        start = self._retrieved
        if self._count is None:
            # Always perform the first query since we don't know the count
            upper_limit = start + 1
        else:
            upper_limit = self._count
        if start < upper_limit:
            end = self._retrieved + self._per_request
            results = self[start:end]
            return results
        return []

    def __len__(self):
        return self.count()

    def __iter__(self):
        return self

    def __getitem__(self, val):
        """
        Override __getitem__ so we can activate our ES call when we try to slice
        """
        start = val.start
        end = val.stop
        raw_results = self._search(start, end)
        for action in self._post_query_actions:
            action(self, raw_results, start, end)
        results = raw_results["hits"]["hits"]
        for wrapper in self._wrappers:
            results = wrapper(results)
        if raw_results.get('aggregations'):
            self._aggregations = raw_results.get('aggregations')
        return results

    def _search(self, start, end):
        conn = self._get_connection()
        pagination_kwargs = self._get_pagination_kwargs(start, end)
        raw_results = conn.search(index=self._index, body=self._query, **pagination_kwargs)
        self._count = self._get_result_count(raw_results)
        self._max_score = self._get_max_score(raw_results)
        return raw_results

    def _get_result_count(self, results):
        return int(results["hits"]["total"])

    def _get_max_score(self, results):
        return results.get("hits", {}).get("max_score")

    def _get_pagination_kwargs(self, start, end):
        size = end - start
        kwargs = {
            'from_': start,  # from is a reserved word, so we use 'from_'
            'size': size
        }
        return kwargs

    def _get_connection(self):
        if not self._conn:
            host_connection_info = self._parse_host_connection_info(self._host)
            self._conn = Elasticsearch(host_connection_info)
        return self._conn

    def _parse_host_connection_info(self, host):
        if isinstance(host, string_types):
            return [{"host": host}]
        if isinstance(host, dict):
            return [host]
        # Default to just using what was given to us
        return host

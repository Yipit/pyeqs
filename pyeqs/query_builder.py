# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from . import Filter
from copy import deepcopy


class QueryBuilder(object):

    def __init__(self, query_string=None):
        super(QueryBuilder, self).__init__()
        self._query = {}
        self._query_dsl = {}
        self._query_string = query_string
        self._filtered = False
        self._filter_dsl = None
        self._scored = False
        self._score_dsl = None
        self._sorted = False
        self._sorting = None
        self._fields = []
        self._build_query()

    def _build_query(self):
        """
        Build the base query dictionary
        """
        if self._query_string:
            self._query_dsl = {"query_string": {"query": self._query_string}}
        else:
            self._query_dsl = {"match_all": {}}

    def _build_filtered_query(self, f, operator):
        """
        Create the root of the filter tree
        """
        self._filtered = True
        if isinstance(f, Filter):
            filter_object = f
        else:
            filter_object = Filter(operator).filter(f)
        self._filter_dsl = filter_object

    def filter(self, f, operator="and"):
        """
        Add a filter to the query

        Takes a Filter object, or a filterable DSL object.
        """
        if self._filtered:
            self._filter_dsl.filter(f)
        else:
            self._build_filtered_query(f, operator)
        return self

    def _build_sorted_query(self):
        self._sorted = True
        self._sorting = []

    def sort(self, sorting):
        if not self._sorted:
            self._build_sorted_query()
        self._sorting.append(sorting)
        return self

    def score(self, script_score, boost_mode="replace"):
        self._scored = True
        self._score_dsl = {
            "function_score": {
                "script_score": script_score,
                "boost_mode": boost_mode
            }
        }
        return self

    def fields(self, fields):
        self._fields.append(fields)

    def _finalize_query(self):
        query = {
            "query": self._query_dsl
        }
        if self._filtered:
            filtered_query = {
                "query": {
                    "filtered": {
                        "filter": self._filter_dsl
                    }
                }
            }
            filtered_query["query"]["filtered"]["query"] = deepcopy(query["query"])
            query = filtered_query

        if self._scored:
            scored_query = {
                "query": self._score_dsl
            }
            scored_query["query"]["function_score"]["query"] = deepcopy(query["query"])
            query = scored_query

        if self._sorted:
            query["sort"] = self._sorting

        if self._fields:
            query["fields"] = self._fields
        return query

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from . import Filter
from copy import deepcopy
from six import string_types
from pyeqs.dsl import MatchAll, QueryString, ScriptScore


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
        self._min_score = None
        self._track_scores = False
        self._sorted = False
        self._sorting = None
        self._fields = []
        self._aggregated = False
        self._aggregation_dsl = None
        self._build_query()

    def _build_query(self):
        """
        Build the base query dictionary
        """
        if isinstance(self._query_string, QueryString):
            self._query_dsl = self._query_string
        elif isinstance(self._query_string, string_types):
            self._query_dsl = QueryString(self._query_string)
        else:
            self._query_dsl = MatchAll()

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

    def score(self, scoring_block, boost_mode="replace", score_mode="multiply", min_score=None, track_scores=False):
        if not self._scored:
            self._scored = True
            self._score_dsl = {
                "function_score": {
                    "functions": [],
                    "boost_mode": boost_mode,
                    "score_mode": score_mode
                }
            }
        if isinstance(scoring_block, ScriptScore):
            self._score_dsl["function_score"]["functions"].append({"script_score": scoring_block})
        else:
            self._score_dsl["function_score"]["functions"].append(scoring_block)
        if min_score is not None:
            self._min_score = min_score
        if track_scores:
            self._track_scores = track_scores
        return self

    def _build_aggregation_query(self, aggregation):
        self._aggregated = True
        return aggregation

    def aggregate(self, aggregation):
        if self._aggregated:
            self._aggregation_dsl.update(aggregation)
        else:
            self._aggregation_dsl = self._build_aggregation_query(aggregation)
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
            if self._min_score is not None:
                scored_query["min_score"] = self._min_score
            if self._track_scores:
                scored_query["track_scores"] = self._track_scores
            scored_query["query"]["function_score"]["query"] = deepcopy(query["query"])
            query = scored_query

        if self._sorted:
            query["sort"] = self._sorting

        if self._fields:
            query["fields"] = self._fields

        if self._aggregated:
            query["aggregations"] = self._aggregation_dsl

        return query

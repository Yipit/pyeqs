# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httpretty
import json
import sure

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Term, Sort, ScriptScore
from tests.helpers import homogeneous


@httpretty.activate
def test_create_queryset_with_host_string():
    """
    Create a queryset with a host given as a string
    """
    # When create a queryset
    t = QuerySet("localhost", index="bar")

    # And I have records
    response = {
       "took": 1,
       "hits": {
          "total": 1,
          "max_score": 1,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "1",
                "_score": 10,
                "_source": {
                   "foo": "bar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }

    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                       body=json.dumps(response),
                       content_type="application/json")

    # When I run a query
    results = t[0:1]

    # Then I see the response.
    len(results).should.equal(1)


@httpretty.activate
def test_create_queryset_with_host_dict():
    """
    Create a queryset with a host given as a dict
    """
    # When create a queryset
    connection_info = {"host": "localhost", "port": 8080}
    t = QuerySet(connection_info, index="bar")

    # And I have records
    good_response = {
       "took": 1,
       "hits": {
          "total": 1,
          "max_score": 1,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "1",
                "_score": 10,
                "_source": {
                   "foo": "bar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }

    bad_response = {
       "took": 1,
       "hits": {
          "total": 0,
          "max_score": None,
          "hits": []
       }
    }
    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                       body=json.dumps(bad_response),
                       content_type="application/json")

    httpretty.register_uri(httpretty.GET, "http://localhost:8080/bar/_search",
                       body=json.dumps(good_response),
                       content_type="application/json")

    # When I run a query
    results = t[0:1]

    # Then I see the response.
    len(results).should.equal(1)
    results[0]["_source"]["foo"].should.equal("bar")


@httpretty.activate
def test_create_queryset_with_host_list():
    """
    Create a queryset with a host given as a list
    """
    # When create a queryset
    connection_info = [{"host": "localhost", "port": 8080}]
    t = QuerySet(connection_info, index="bar")

    # And I have records
    good_response = {
       "took": 1,
       "hits": {
          "total": 1,
          "max_score": 1,
          "hits": [
             {
                "_index": "bar",
                "_type": "baz",
                "_id": "1",
                "_score": 10,
                "_source": {
                   "foo": "bar"
                },
                "sort": [
                   1395687078000
                ]
             }
          ]
       }
    }

    bad_response = {
       "took": 1,
       "hits": {
          "total": 0,
          "max_score": None,
          "hits": []
       }
    }
    httpretty.register_uri(httpretty.GET, "http://localhost:9200/bar/_search",
                       body=json.dumps(bad_response),
                       content_type="application/json")

    httpretty.register_uri(httpretty.GET, "http://localhost:8080/bar/_search",
                       body=json.dumps(good_response),
                       content_type="application/json")

    # When I run a query
    results = t[0:1]

    # Then I see the response.
    len(results).should.equal(1)
    results[0]["_source"]["foo"].should.equal("bar")

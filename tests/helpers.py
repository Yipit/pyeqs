# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from distutils.version import StrictVersion
from nose.plugins.skip import SkipTest

from elasticsearch import (
    Elasticsearch
)

ELASTICSEARCH_URL = "localhost"
conn = Elasticsearch(ELASTICSEARCH_URL)
index_name = "foo"
default_doc_type = "my_doc_type"


def homogeneous(a, b):
    json.dumps(a, sort_keys=True).should.equal(json.dumps(b, sort_keys=True))


def heterogeneous(a, b):
    json.dumps(a, sort_keys=True).shouldnt.equal(json.dumps(b, sort_keys=True))


def add_document(index, document, **kwargs):
    kwargs = _set_doc_type(kwargs)
    conn.create(index=index, body=document, refresh=True, **kwargs)


def clean_elasticsearch(context):
    _delete_es_index(index_name)


def prepare_elasticsearch(context):
    clean_elasticsearch(context)
    _create_foo_index()
    conn.cluster.health(wait_for_status='yellow', index=index_name)


def _create_foo_index():
    mapping = _get_mapping(index=index_name)
    conn.indices.create(index=index_name, ignore=400, body=mapping)
    conn.indices.refresh(index=index_name)


def _delete_es_index(index):
    conn.indices.delete(index=index, ignore=[400, 404])


def _get_mapping(index, **kwargs):
    kwargs = _set_doc_type(kwargs)
    doc_type = kwargs['doc_type']
    mapping = {
        "mappings": {
            doc_type: {
                "properties": {
                    "location": {
                        "type": "geo_point"
                    },
                    "foo_loc": {
                        "type": "geo_point"
                    },
                    "child": {
                        "type": "nested"
                    }
                }
            }
        }
    }
    return mapping


def _set_doc_type(kwargs):
    if "doc_type" not in kwargs:
        # Allow overriding doc type defaults
        kwargs["doc_type"] = default_doc_type
    return kwargs


prepare_data = [
    prepare_elasticsearch
]

cleanup_data = [
    clean_elasticsearch
]


def version_tuple(v):
    return tuple(map(int, (v.split("."))))


class requires_es_gte(object):
    """
    Decorator for requiring Elasticsearch version
    greater than or equal to 'version'
    """
    def __init__(self, version):
        self.version = version

    def __call__(self, test):
        es_version_string = os.environ.get("ES_VERSION", None)
        if es_version_string is None:  # Skip check if we don't know our version
            return test
        es_version = StrictVersion(es_version_string)
        required = StrictVersion(self.version)
        if es_version >= required:
            return test
        raise SkipTest

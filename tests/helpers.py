# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from pyelasticsearch import (
        ElasticSearch,
        ElasticHttpNotFoundError
)

ELASTICSEARCH_URL = "http://localhost:9200"
conn = ElasticSearch(ELASTICSEARCH_URL)


def homogeneous(a, b):
    json.dumps(a).should.equal(json.dumps(b))


def heterogeneous(a, b):
    json.dumps(a).shouldnt.equal(json.dumps(b))


def add_document(index, document):
    conn.index(index, "foo", document, id=None, refresh=True)


def clean_elasticsearch(context):
    _delete_es_index("foo")


def prepare_elasticsearch(context):
    clean_elasticsearch(context)
    _create_foo_index()
    conn.health(wait_for_status='yellow')


def _create_foo_index():
    conn.create_index("foo")


def _delete_es_index(index):
    try:
        conn.delete_index(index)
    except ElasticHttpNotFoundError:
        pass


prepare_data = [
    prepare_elasticsearch
]

cleanup_data = [
    clean_elasticsearch
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from elasticsearch import (
        Elasticsearch,
        TransportError
)

ELASTICSEARCH_URL = "localhost"
conn = Elasticsearch(ELASTICSEARCH_URL)


def homogeneous(a, b):
    json.dumps(a).should.equal(json.dumps(b))


def heterogeneous(a, b):
    json.dumps(a).shouldnt.equal(json.dumps(b))


def add_document(index, document, **kwargs):
    if "doc_type" not in kwargs:
        # Allow overriding doc type defaults
        doc_type = "my_doc_type"
        kwargs["doc_type"] = doc_type
    conn.create(index=index, body=document, refresh=True, **kwargs)


def clean_elasticsearch(context):
    _delete_es_index("foo")


def prepare_elasticsearch(context):
    clean_elasticsearch(context)
    _create_foo_index()
    conn.cluster.health(wait_for_status='yellow')


def _create_foo_index():
    conn.indices.create(index="foo", ignore=400)


def _delete_es_index(index):
    conn.indices.delete(index=index, ignore=[400, 404])


prepare_data = [
    prepare_elasticsearch
]

cleanup_data = [
    clean_elasticsearch
]

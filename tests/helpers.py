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


def add_document(index, document):
    document_type = "my_doc_type"
    conn.create(index=index, doc_type=document_type, body=document, id=None, refresh=True)


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

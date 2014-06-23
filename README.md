# PyEQS [![Build Status](https://travis-ci.org/Yipit/pyeqs.svg?branch=master)](https://travis-ci.org/Yipit/pyeqs) [![Coverage Status](https://coveralls.io/repos/Yipit/pyeqs/badge.png)](https://coveralls.io/r/Yipit/pyeqs)

#### Python Elasticsearch QuerySets

A python library to simplify building complex Elasticsearch JSON queries.  Based on the Django QuerySet API, backed by the [official python elasticsearch library](https://github.com/elasticsearch/elasticsearch-py).  Supports Elasticsearch `1.0+`.

This is an attempt to provide an interface familiar to users of Django Querysets.  Due to the differences in the backends it was impossible to mirror the Queryset API and maintain full search functionality.  Be aware when using this library that the interfaces may not have the same trade-offs and caveats.

#### Current Development Status

Currently pre `v1.0`, so the API is not locked in.  This project aims to follow [semantic versioning](http://semver.org/) once it reaches a stable API.  Issues may arise as the backend `elasticsearch-py` library locks its versions to **Elasticsearch** releases.

## Installation

```bash
pip install pyeqs
```

## Usage

Check out the [API Reference](https://github.com/Yipit/pyeqs/blob/master/API_REFERENCE.md) for examples.

## Alternatives

#### Python
* [ElasticUtils](http://elasticutils.readthedocs.org/en/latest/): A library by Mozilla uses a syntax leveraging built-in &, | and ~ to construct queries.
* [Elasticsearch-dsl-py](https://github.com/elasticsearch/elasticsearch-dsl-py): A library by Elasticsearch that is similar and compatible with ElasticUtils.
* [Django-Haystack](https://github.com/toastdriven/django-haystack): A library that wraps multiple search backends and presents them in the same interface as Django models.  In my experience a very all-in-one solution that makes it hard to manipulate Elasticsearch directly, but wonderful when you need the feature set.

#### Ruby
* [Plunk](https://github.com/elbii/plunk): A ruby library to allow you to write strings to queries that have more power than simple 'query string' requests

#### Haskell
* [Bloodhound](https://github.com/bitemyapp/bloodhound/): A basic Elasticsearch Client that also has the ability to leverage the language's built-in operators to construct queries.

# PyEQS [![Build Status](https://travis-ci.org/Yipit/pyeqs.svg?branch=master)](https://travis-ci.org/Yipit/pyeqs) [![Coverage Status](https://coveralls.io/repos/Yipit/pyeqs/badge.png)](https://coveralls.io/r/Yipit/pyeqs)

#### Python Elasticsearch QuerySets

A python library to simplify building complex Elasticsearch JSON queries.  Based on the Django QuerySet API, backed by the [official python elasticsearch library](https://github.com/elasticsearch/elasticsearch-py).  Supports Elasticsearch `1.0+`.

#### Current Development Status

Currently pre `v1.0`, so the API is not locked in.  This project aims to follow [semantic versioning](http://semver.org/) once it reaches a stable API.  The only issues may arise as the backend `elasticsearch-py` library locks its versions to *Elasticsearch* releases.

## Installation

```bash
pip install pyeqs
```

## Usage

#### Simple querying

```python
from pyeqs import QuerySet
qs = QuerySet("127.0.0.1", index="my_index")
print qs._query
"""
{
  'query': {
    'match_all': {}
  }
}
"""
```

```python
from pyeqs import QuerySet
qs = QuerySet("127.0.0.1", query="cheese", index="my_index")
print qs._query
"""
{
  'query': {
    'query_string': {
      'query': 'cheese'
    }
  }
}
"""
```

#### Filtering

```python
from pyeqs import QuerySet
from pyeqs.dsl import Term, Type
qs = QuerySet("127.0.0.1", index="my_index")
qs.filter(Term("foo", "bar"), operator="or").filter(Type("baz"))
print qs._query
"""
{
  'query': {
    'filtered': {
      'filter': {
        'or': [
          {
            'term': {
              'foo': 'bar'
            }
          },
          {
            'type': {
              'value': 'baz'
            }
          }
        ]
      },
      'query': {
        'match_all': {}
      }
    }
  }
}
"""
```

#### Boolean Filters

```python
from pyeqs import QuerySet, Bool
from pyeqs.dsl import Sort
qs = QuerySet("127.0.0.1", index="my_index")
b = Bool()
b.must(Term("foo", "bar"))
qs.filter(b)
```

#### Sorting

```python
from pyeqs import QuerySet
from pyeqs.dsl import Sort
qs = QuerySet("127.0.0.1", index="my_index")
qs.order_by(Sort("_id", order="desc"))
```

#### Scoring

```python
from pyeqs import QuerySet
from pyeqs.dsl import ScriptScore
qs = QuerySet("127.0.0.1", index="my_index")
qs.score(ScriptScore("score = foo + bar;", lang="mvel", params={"bar": 1}))
```

#### Wrapping Results

```python
from pyeqs import QuerySet
from pyeqs.dsl import Term
qs = QuerySet("127.0.0.1", index="my_index")
qs.filter(Term("foo", 1)
qs.wrapper(lambda x: x['_id'])
```

#### Limiting Returned Fields

```python
from pyeqs import QuerySet
qs = QuerySet("127.0.0.1", index="my_index")
qs.only('_id')
```

#### Reusing Querysets

```python
from pyeqs import QuerySet
from pyeqs.dsl import Terms, Term
qs = QuerySet("127.0.0.1", index="my_index")
qs.filter(Terms("foo", ["bar", "baz"]))

# Duplicate the Queryset and do more filters
only_bar = qs.objects.filter(Term("foo", "bar"))

only_baz = qs.objects.filter(Term("foo", "baz"))
```

#### Slicing Querysets

```python
from pyeqs import QuerySet
from pyeqs.dsl import Term
qs = QuerySet("127.0.0.1", index="my_index")
qs.filter(Term("foo", "bar"))
results = qs[0:10]  # Uses from/size in the background
```

#### Iterating over Quersets

```python
from pyeqs import QuerySet
from pyeqs.dsl import Term
qs = QuerySet("127.0.0.1", index="my_index")
qs.filter(Term("foo", "bar"))
for result in qs:
  print result['_source']
  # Builds a cache of 10 results at a time and iterates
```

#### Getting Counts

```python
from pyeqs import QuerySet
from pyeqs.dsl import Term
qs = QuerySet("127.0.0.1", index="my_index")
qs.filter(Term("foo", "bar"))
qs.count()   # None, since we haven't queried
qs[0:10]
qs.count()   # Returns number of hits
```

## Alternatives

#### Python
* [ElasticUtils](http://elasticutils.readthedocs.org/en/latest/): A library by Mozilla uses a syntax leveraging built in &, | and ~ to construct queries.
* [Elasticsearch-dsl-py](https://github.com/elasticsearch/elasticsearch-dsl-py): A library by Elasticsearch that is similar and compatible with ElasticUtils.

#### Ruby
* [Plunk](https://github.com/elbii/plunk): A ruby library to allow you to write strings to queries that have more power than simple 'query string' requests

#### Haskell
* [Bloodhound](https://github.com/bitemyapp/bloodhound/): A basic Elasticsearch Client that also has the ability to leverage the languages built in operators to construct queries.

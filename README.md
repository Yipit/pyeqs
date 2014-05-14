# PyEQS [![Build Status](https://travis-ci.org/Yipit/pyeqs.svg)](https://travis-ci.org/Yipit/pyeqs)

#### Python Elasticsearch QuerySets

A python library to simplify building complex Elasticsearch JSON queries.  Based on the Django QuerySet API.  Currently backed by `pyelasticsearch` but moving towards `elasticsearch.py`.

## Installation 

```bash
pip install pyeqs
```

## Usage

Simple querying

```python
from pyeqs import QuerySet
qs = QuerySet("http://localhost:9200", index="my_index")
print qs._query
"""{
  'query': {
    'match_all': {}
  }
}"""
```

Simple Filtering

```python
from pyeqs import QuerySet
from pyeqs.dsl import Term
qs = QuerySet("http://localhost:9200", index="my_index")
qs.filter(Term("foo", "bar"))
print qs._query
"""{
  'query': {
    'filtered': {
      'filter': {
        'and': [
          {
            'term': {
              'foo': 'bar'
            }
          }
        ]
      },
      'query': {
        'match_all': {}
      }
    }
  }
}"""
```

## Contributing

* Fork the `git` repo
* Download the forked `git` repo
* Create a branch for your changes
* Link the `pre-commit` hook to `.git/hooks/pre-commit`
* Run the tests to make sure everything works, before you make changes
* Change the code for your PR
* Write (or modify) tests to make sure your changes work
* Submit a Pull Request

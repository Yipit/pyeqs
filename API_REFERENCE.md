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

#### Location Sorting

Assuming a set of records with a `location` field mapped as a `geo_point`:

```python
from pyeqs import QuerySet
from pyeqs.dsl import Sort
qs = QuerySet("127.0.0.1", index="my_index")
qs.order_by(Sort("location", location=[40.0, 74.5]))
```

The parameter passed to the `location` kwarg can be any format that elasticsearch accepts.


#### Scoring

Single Scoring Functions

```python
from pyeqs import QuerySet
from pyeqs.dsl import ScriptScore
qs = QuerySet("127.0.0.1", index="my_index")
qs.score(ScriptScore("score = foo + bar;", lang="mvel", params={"bar": 1}))
```

Multiple Scoring Functions


```python
from pyeqs import QuerySet
from pyeqs.dsl import ScriptScore
qs = QuerySet("127.0.0.1", index="my_index")
qs.score(ScriptScore("score = foo + bar;", lang="mvel", params={"bar": 1}))
qs.score({"boost": 10, "filter": {"term": {"foo": "bar"}}})
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

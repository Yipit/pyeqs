### `0.10.0`

* Add `aggregations` functionality

### `0.9.0`

* Properly increment version number for SemVer.

### `0.8.2`

* Add `post_query_actions` to provide hooks for logging and debugging inside the iterator.

### `0.8.1`

* Add `score_mode` kwarg to scoring blocks.

### `0.8.0`

* Add Exists Block
* Update `function_score` to support multiple scoring blocks.

### `0.7.4`

* Add ability to sort on `location` fields.  See the API Reference for details.

### `0.7.3`

* Add `min_score` and `track_scores` options to `score`.

### `0.7.2`

* Add `QuerySet` to DSL

### `0.7.1`

* Add `execution` option to Terms DSL

### `0.7.0`

* Add python 3 support

### `0.6.3`

* Revent cloning change

### `0.6.2`

* Force creation of clones as `QuerySet` objects

### `0.6.1`

* Fix broken syntax around `clone` method

### `0.6.0`

* Add `missing` to DSL

### `0.5.1`

* Allow custom field names in GeoDistance queries

### `0.5.0`

* Add `match_all` to DSL.
* Switch default query to use new DSL match all

### `0.4.0`

* Add option to specify 'missing' when creating a sort block

### `0.3.3`

* More flexible passing of connection parameters to backend library

### `0.3.2`

* Don't lock `six` version so explicitly.

### `0.3.1`

* Don't override `range` keyword when constructing `Range` dict.

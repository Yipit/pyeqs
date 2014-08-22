# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyeqs.dsl import Aggregations
from tests.helpers import homogeneous


def test_add_agg():
    """
    Create aggregations block
    """
    # When add an agg block
    t = Aggregations("agg_name", "field_name", "metric")

    # Then I see correct json
    results = {
        "agg_name": {
            "metric": {"field": "field_name"}
        }
    }

    homogeneous(t, results)


def test_add_agg_with_size():
    """
    Create aggregations block specifying size
    """
    # When add a terms agg block w/ size
    t = Aggregations("agg_name", "field_name", "terms", size=1)

    # Then I see correct json
    results = {
        "agg_name": {
            "terms": {
                "field": "field_name",
                "order": {"_count": "desc"},
                "min_doc_count": 1,
                "size": 1
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_with_order():
    """
    Create aggregations block specifying order type and direction
    """
    # When add a terms agg block w/ size
    t = Aggregations("agg_name", "field_name", "terms", order_type="_term", order_dir="asc")

    # Then I see correct json
    results = {
        "agg_name": {
            "terms": {
                "field": "field_name",
                "order": {"_term": "asc"},
                "min_doc_count": 1,
                "size": 0
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_with_min_doc_count():
    """
    Create aggregations block specifying the min_doc_count
    """
    # When add a terms agg block w/ size
    t = Aggregations("agg_name", "field_name", "terms", min_doc_count=10)

    # Then I see correct json
    results = {
        "agg_name": {
            "terms": {
                "field": "field_name",
                "order": {"_count": "desc"},
                "min_doc_count": 10,
                "size": 0
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_nested():
    """
    Create nested aggregations block
    """
    # When add a nested_path with agg block
    t = Aggregations("agg_name", "field_name", "metric", nested_path="nested_doc")

    # The I see correct json
    results = {
        "nested_doc": {
            "nested": {"path": "nested_doc"},
            "aggregations": {
                "agg_name": {"metric": {"field": "nested_doc.field_name"}},
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_nested_with_size():
    """
    Create nested aggregations block specifying size
    """
    # When add a nested_path with terms agg block w/ size
    t = Aggregations("agg_name", "field_name", "terms", size=1,
                     nested_path="nested_doc")

    # The I see correct json
    results = {
        "nested_doc": {
            "nested": {"path": "nested_doc"},
            "aggregations": {
                "agg_name": {"terms": {
                    "field": "nested_doc.field_name",
                    "order": {"_count": "desc"},
                    "min_doc_count": 1,
                    "size": 1
                }}
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_nested_with_order():
    """
    Create nested aggregations block specifying order type and direction
    """
    # When add a nested_path with terms agg block w/ size
    t = Aggregations("agg_name", "field_name", "terms", order_type="_term", order_dir="asc",
                     nested_path="nested_doc")

    # The I see correct json
    results = {
        "nested_doc": {
            "nested": {"path": "nested_doc"},
            "aggregations": {
                "agg_name": {"terms": {
                    "field": "nested_doc.field_name",
                    "order": {"_term": "asc"},
                    "min_doc_count": 1,
                    "size": 0
                }}
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_nested_with_min_doc_count():
    """
    Create nested aggregations block specifying min_doc_count
    """
    # When add a nested_path with terms agg block w/ size
    t = Aggregations("agg_name", "field_name", "terms", min_doc_count=10,
                     nested_path="nested_doc")

    # The I see correct json
    results = {
        "nested_doc": {
            "nested": {"path": "nested_doc"},
            "aggregations": {
                "agg_name": {"terms": {
                    "field": "nested_doc.field_name",
                    "order": {"_count": "desc"},
                    "min_doc_count": 10,
                    "size": 0
                }}
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_filtered():
    """
    Create an aggregations block with filter
    """
    # With a filter
    filter_value = {"filter_type": {"other_field": {"comparison": "value"}}}

    # When add a filtered agg block
    t = Aggregations("agg_name", "field_name", "metric", filter_val=filter_value,
                     filter_name="filter_on_other")

    # Then I see correct json
    results = {
        "filter_on_other": {
            "filter": filter_value,
            "aggregations": {
                "agg_name": {"metric": {"field": "field_name"}}
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_global():
    """
    Create an aggregations block that is global
    """
    # When add a global agg block
    t = Aggregations("agg_name", "field_name", "metric", global_name="global_agg")

    # Then I see correct json
    results = {
        "global_agg": {
            "global": {},
            "aggregations": {
                "agg_name": {"metric": {"field": "field_name"}}
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_range():
    """
    Create an aggregations block for a range
    """
    # When add an agg block w/ range
    range_list = [1, 2, 3]
    t = Aggregations("agg_name", "field_name", "metric", range_list=range_list, range_name="my_ranges")

    # Then I see the correct json
    results = {
        "my_ranges": {
            "range": {
                "field": "field_name",
                "ranges": [
                    {"to": 1},
                    {"from": 1, "to": 2},
                    {"from": 2, "to": 3},
                    {"from": 3}
                ]
            }}
    }

    homogeneous(t, results)

    # Also works without a given range_name
    t = Aggregations("agg_name", "field_name", "metric", range_list=range_list)

    # Then I see the correct json
    results = {
        "field_name_ranges": {
            "range": {
                "field": "field_name",
                "ranges": [
                    {"to": 1},
                    {"from": 1, "to": 2},
                    {"from": 2, "to": 3},
                    {"from": 3}
                ]
            }}
    }

    homogeneous(t, results)


def test_add_agg_histogram():
    """
    Create an aggregations block w/ histogram intervals
    """
    # Whan add an agg block w/ interval
    t = Aggregations("agg_name", "field_name", "metric", histogram_interval=20)

    # Then I see correct json
    results = {
        "agg_name": {
            "histogram": {
                "field": "field_name",
                "interval": 20,
                "order": {"_key": "desc"},
                "min_doc_count": 1
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_histogram_with_order():
    """
    Create an aggregations block w/ histogram intervals and order type/direction
    """
    # Whan add an agg block w/ interval
    t = Aggregations("agg_name", "field_name", "metric", histogram_interval=20,
                     order_type="_count", order_dir="asc")

    # Then I see correct json
    results = {
        "agg_name": {
            "histogram": {
                "field": "field_name",
                "interval": 20,
                "order": {"_count": "asc"},
                "min_doc_count": 1
            }
        }
    }

    homogeneous(t, results)


def test_add_agg_histogram_with_min_doc_count():
    """
    Create an aggregations block w/ histogram intervals and min_doc_count
    """
    # Whan add an agg block w/ interval
    t = Aggregations("agg_name", "field_name", "metric", histogram_interval=20,
                     min_doc_count=10)

    # Then I see correct json
    results = {
        "agg_name": {
            "histogram": {
                "field": "field_name",
                "interval": 20,
                "order": {"_key": "desc"},
                "min_doc_count": 10
            }
        }
    }

    homogeneous(t, results)

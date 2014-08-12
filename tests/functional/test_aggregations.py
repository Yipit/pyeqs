# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Aggregations, Range
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_search_aggregation(context):
    """
    Search with aggregation
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do an aggregated search
    t.aggregate(aggregation=Aggregations("foo_attrs", "bar", "terms"))
    t[0:10]

    # Then I get a the expected results
    t.aggregations().should.have.key('foo_attrs')
    t.aggregations()['foo_attrs'].should.have.key("buckets").being.equal([
        {u'key': u'baz', u'doc_count': 1}, {u'key': u'bazbaz', u'doc_count': 1}])


@scenario(prepare_data, cleanup_data)
def test_search_aggregation_with_size(context):
    """
    Search with aggregation w/ specified size
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "baz"})
    add_document("foo", {"bar": "bazbaz"})
    add_document("foo", {"bar": "bazbar"})

    # And I do an aggregated search
    t.aggregate(aggregation=Aggregations("foo_attrs", "bar", "terms", size=1))
    t[0:10]

    # Then I get a the expected results
    t.aggregations().should.have.key('foo_attrs')
    t.aggregations()['foo_attrs'].should.have.key("buckets").being.equal([
        {u'key': u'baz', u'doc_count': 2}])


@scenario(prepare_data, cleanup_data)
def test_search_multi_aggregations(context):
    """
    Search with multiple aggregations
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do an aggregated search on two dimensions
    t.aggregate(aggregation=Aggregations("bar_attrs", "bar", "terms"))
    t.aggregate(aggregation=Aggregations("missing_foo", "foo", "missing"))
    t[0:10]

    # Then I get a the expected results
    t.aggregations().should.have.key("missing_foo").being.equal({u'doc_count': 1})
    t.aggregations().should.have.key("bar_attrs")
    t.aggregations()['bar_attrs'].should.have.key("buckets").being.equal([
        {u'key': u'bazbaz', u'doc_count': 2}, {u'key': u'baz', u'doc_count': 1}])


@scenario(prepare_data, cleanup_data)
def test_search_nested_aggregations(context):
    """
    Search with nested aggregations
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are nested records
    add_document("foo", {"child": [{"stuff": "yep", "bazbaz": 10}], "foo": "foo"})
    add_document("foo", {"child": [{"stuff": "nope", "bazbaz": 1}], "foo": "foofoo"})

    # And I do a nested
    t.aggregate(aggregation=Aggregations("best_bazbaz", "bazbaz", "max", nested_path="child"))
    t[0:10]

    # The I get the expected results
    t.aggregations().should.have.key("child").being.equal({'best_bazbaz': {'value': 10.0}, 'doc_count': 2})


@scenario(prepare_data, cleanup_data)
def test_search_nested_terms_aggregations_with_size(context):
    """
    Search with nested terms aggregation and a specified size
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are nested records
    add_document("foo", {"child": [{"stuff": "yep", "bazbaz": "type0"}], "foo": "foo"})
    add_document("foo", {"child": [{"stuff": "yep", "bazbaz": "type0"}], "foo": "foo"})
    add_document("foo", {"child": [{"stuff": "nope", "bazbaz": "type1"}], "foo": "foofoo"})
    add_document("foo", {"child": [{"stuff": "nope", "bazbaz": "type2"}], "foo": "foofoo"})

    # And I do a nested
    t.aggregate(aggregation=Aggregations("baz_types", "bazbaz", "terms",
                                         nested_path="child", size=1))
    t[0:10]

    # The I get the expected results
    t.aggregations().should.have.key("child").being.equal({
        u'baz_types': {
            u'buckets': [{u'doc_count': 2, u'key': u'type0'}]
        },
        u'doc_count': 4
    })


@scenario(prepare_data, cleanup_data)
def test_search_filtered_aggregations(context):
    """
    Search with filtered aggregations
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 0, "foo": "baz"})
    add_document("foo", {"bar": 0, "foo": "baz"})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3, "foo": "bazbaz"})
    add_document("foo", {"bar": 5, "foo": "foobar"})
    add_document("foo", {"bar": 5})
    add_document("foo", {"bar": 5, "foo": "foobaz"})
    add_document("foo", {"bar": 9})

    # And I do a filtered
    f = Filter().filter(Range("bar", gte=5))
    t.aggregate(aggregation=Aggregations("missing_foo", "foo", "missing",
                                         filter_val=f, filter_name="high_bar"))
    t[0:10]

    # Then I get the expected results
    t.aggregations().should.have.key("high_bar")
    t.aggregations()["high_bar"].should.have.key("missing_foo").being.equal(
        {u'doc_count': 2})
    t.aggregations()["high_bar"]["doc_count"].should.equal(4)


@scenario(prepare_data, cleanup_data)
def test_search_global_aggregations(context):
    """
    Search with global aggregations
    """
    # With a specific query
    # q = QueryBuilder(query_string=QueryString(query={"match": {"foo_attr": "yes"}}))

    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "foo_attr": "yes"})
    add_document("foo", {"bar": "bazbaz", "foo_attr": "no"})
    add_document("foo", {"bar": "bazbaz"})

    # And I do a global
    t.aggregate(aggregation=Aggregations("foo_attrs", "bar", "terms", global_name="all_bar"))
    t[0:10]

    # I get the expected results
    t.aggregations().should.have.key("all_bar").being.equal({
        u'foo_attrs': {u'buckets': [
            {u'key': u'bazbaz', u'doc_count': 2},
            {u'key': u'baz', u'doc_count': 1}
        ]},
        u'doc_count': 3})


@scenario(prepare_data, cleanup_data)
def test_search_range_aggregations(context):
    """
    Search with aggregations for ranges
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 1, "foo": "foo"})
    add_document("foo", {"bar": 2, "foo": "foo"})
    add_document("foo", {"bar": 2})

    # When I do a ranged aggregation
    range_list = [0, 1, 2, 3]
    t.aggregate(aggregation=Aggregations("bar_types", "bar", "metric", range_list=range_list))
    t[0:10]

    # I get the expected results
    t.aggregations().should.have.key("bar_ranges")
    t.aggregations()["bar_ranges"].should.have.key("buckets").being.equal([
        {u'to': 0.0, u'doc_count': 0},
        {u'to': 1.0, u'from': 0.0, u'doc_count': 0},
        {u'to': 2.0, u'from': 1.0, u'doc_count': 1},
        {u'to': 3.0, u'from': 2.0, u'doc_count': 2},
        {u'from': 3.0, u'doc_count': 0}])

    # And I should be able to name it if I want
    t.aggregate(aggregation=Aggregations("bar_types", "bar", "metric",
                                         range_list=range_list, range_name="my_unique_range"))
    t[0:10]

    # I get the expected results
    t.aggregations().should.have.key("my_unique_range")
    t.aggregations()["my_unique_range"].should.have.key("buckets").being.equal([
        {u'to': 0.0, u'doc_count': 0},
        {u'to': 1.0, u'from': 0.0, u'doc_count': 0},
        {u'to': 2.0, u'from': 1.0, u'doc_count': 1},
        {u'to': 3.0, u'from': 2.0, u'doc_count': 2},
        {u'from': 3.0, u'doc_count': 0}])


@scenario(prepare_data, cleanup_data)
def test_search_histogram_aggregations(context):
    """
    Search with aggregations that have histograms
    """
    # When create a query block
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": 0, "foo": "baz"})
    add_document("foo", {"bar": 0, "foo": "baz"})
    add_document("foo", {"bar": 2})
    add_document("foo", {"bar": 3, "foo": "bazbaz"})
    add_document("foo", {"bar": 5, "foo": "foobar"})
    add_document("foo", {"bar": 5})
    add_document("foo", {"bar": 5, "foo": "foobaz"})
    add_document("foo", {"bar": 9})

    # When I do a histogram aggregation
    t.aggregate(aggregation=Aggregations("bar_buckets", "bar", "metric", histogram_interval=2))
    t[0:10]

    # I get the expected results
    t.aggregations().should.have.key("bar_buckets")
    t.aggregations()["bar_buckets"].should.have.key("buckets").being.equal([
        {u'key': 0, u'doc_count': 2},
        {u'key': 2, u'doc_count': 2},
        {u'key': 4, u'doc_count': 3},
        {u'key': 8, u'doc_count': 1}])

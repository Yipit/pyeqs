# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class Aggregations(dict):

    def __init__(self, agg_name, field_name, metric, size=0, filter_val=None, filter_name=None,
                 global_name=None, nested_path=None, range_list=None, range_name=None,
                 histogram_interval=None):
        super(Aggregations, self).__init__()
        self.agg_name = agg_name
        self.field_name = field_name
        self.metric = metric
        self.size = size
        self.filter_val = filter_val
        self.filter_name = filter_name
        self.global_name = global_name
        self.nested_path = nested_path
        self.range_list = range_list
        self.range_name = range_name
        self.interval = histogram_interval
        self._build_dict()

    def _build_dict(self):
        if self.nested_path:
            self[self.nested_path] = self._nesting()
        else:
            self[self.agg_name] = {self.metric: {"field": self.field_name}}
            if self.metric == "terms":
                self[self.agg_name][self.metric].update({"size": self.size})

        if self.range_list:
            if not self.range_name:
                range_name = "{name}_ranges".format(name=self.field_name)
            else:
                range_name = self.range_name
            self[range_name] = {"range": {
                "field": self.field_name,
                "ranges": self._ranging()
            }}
            self.pop(self.agg_name)
        if self.interval:
            self[self.agg_name]["histogram"] = {
                "field": self.field_name,
                "interval": self.interval
            }
            self[self.agg_name].pop(self.metric)
        elif self.filter_val and self.filter_name:
            self[self.filter_name] = {'filter': self.filter_val, 'aggregations': {}}
            self[self.filter_name]['aggregations'][self.agg_name] = self.pop(self.agg_name)
        elif self.global_name:
            self[self.global_name] = {"global": {}, "aggregations": {}}
            self[self.global_name]['aggregations'][self.agg_name] = self.pop(self.agg_name)

    def _nesting(self):
        nesting = {
            "nested": {"path": self.nested_path},
            "aggregations": {
                self.agg_name: {
                    self.metric: {"field": "{path}.{name}".format(path=self.nested_path, name=self.field_name)}
                }}
        }
        if self.metric == "terms":
            nesting["aggregations"][self.agg_name][self.metric].update({"size": self.size})
        return nesting

    def _ranging(self):
        """
        Should be a list of values to designate the buckets
        """
        agg_ranges = []
        for i, val in enumerate(self.range_list):
            if i == 0:
                agg_ranges.append({"to": val})
            else:
                previous = self.range_list[i - 1]
                agg_ranges.append({"from": previous, "to": val})

            if i + 1 == len(self.range_list):
                agg_ranges.append({"from": val})
        return agg_ranges

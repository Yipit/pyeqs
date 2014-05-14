# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json


def homogeneous(a, b):
    json.dumps(a).should.equal(json.dumps(b))


def heterogeneous(a, b):
    json.dumps(a).shouldnt.equal(json.dumps(b))

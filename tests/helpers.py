# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

def compare(a, b):
    json.dumps(a).should.equal(json.dumps(b))

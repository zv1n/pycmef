#!/usr/bin/env python

import sys

import json
from yaml import safe_load

class DataSet: 
  def __init__(self, dict):
    self.data = dict

  def to_json(self, key = None):
    if key is None:
      return json.dumps(self.data)
    else:
      return json.dumps(self.data.get(key, None))

if __name__ == "__main__":
  import sys
  with open(sys.argv[1], 'r') as fh:
    ds = json.load(fh)
    print DataSet(ds).to_json(sys.argv[2])
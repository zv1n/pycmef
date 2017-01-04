#!/usr/bin/env python

import sys, json
from yaml import safe_load

class DataSet:
  def __init__(self, data):
    self.data = data or {}
    self.condition = None
    self.process()

  def print_stats(self):
    print ', '.join([key for key in self.processed.keys()])
    for key in self.processed:
      print 'Key: %s Length: %s' % (key, len(self.processed[key]))

  def set_condition(self, condition):
    self.condition = condition

  def process(self):
    self.processed = {}

    for key in self.data:
      self.process_key(key)

  def process_key(self, key):
    plist = []

    for item in self.data[key]:
      plist.extend(self.permute_item(item))

    self.processed[key] = plist

  def permute_item(self, item):
    items = [item]
    permutations = {
      'images': 'image',
      'questions': 'question'
    }

    for key in permutations:
      items = self.permute_on(key, permutations[key], items)

    return items

  def permute_on(self, key, to_key, items):
    result = []

    for item in items:
      if key not in item:
        result.append(item)
      else:
        permute_me = item.pop(key, None)
        for perm in permute_me:
          new_item = dict(item)
          new_item[to_key] = perm
          result.append(new_item)

    return result

  def get_set(self, dset):
    if dset is None:
      return []

    try:
      condition_set = None

      if self.condition is not None:
        # Allow for data sets to be chosen by condition.
        set_name = "%s:%s" % (dset, self.condition)
        condition_set = self.processed.get(set_name, None)

        # Prefer the conditional set over a raw set name
        if condition_set is not None:
          return condition_set

      if condition_set is None:
        return self.processed[dset]
    except KeyError:
      raise Exception("The requested dataset (%s) does not exist!" % dset)

  def has_set(self, dset):
    return (self.processed.get(dset, None) is not None)

  def to_json(self, key = None):
    if key is None:
      return json.dumps(self.processed)
    else:
      return json.dumps(self.processed.get(key, None))

if __name__ == "__main__":
  if (len(sys.argv) not in (2,3)):
    print('usage: dataset.py <dataset.json> [set]')
    sys.exit(1)

  with open(sys.argv[1], 'r') as fh:
    ds = json.load(fh)

    if (len(sys.argv) > 2):
      print DataSet(ds).to_json(sys.argv[2])
    else:
      DataSet(ds).print_stats()

    print 'Complete.'

#!/usr/bin/env python

import sys, json, os

from pycmef.iterators import *

class DataIterationMixin:
  iterators = [
    SequentialIterator,
    RandomIterator,
    RandomGroup
  ]

  iteration = -1

  def configure(self):
    self.set_count = self.sub_data.get('sets', 1)
    self.this_set = self.sub_data.get('data', None)
    self.selected_data = self.parent.data.get_set(self.this_set)

    default_iter = 1

    if self.selected_data is not None:
      default_iter = len(self.selected_data)

    self.iter_count = self.sub_data.get('iterations', default_iter)

    self.select_iterator()

  def data_to_json(self):
    try:
      return json.dumps(self.current_data)
    except AttributeError:
      return '{}'

  def dataset_to_json(self):
    try:
      return json.dumps(self.selected_data)
    except AttributeError:
      return '{}'

  def should_repeat(self):
    print "MAX: %s CUR: %s" % (self.iter_count, self.iteration)
    return (self.iter_count > self.iteration) and (not self.iterator.done())

  def next(self):
    self.iteration += 1

    if self.selected_data is None:
      self.current_data = None
      return

    try:
      self.load_data()
      return True
    except KeyError, IndexError:
      return False

  def load_data(self):
    if not self.selected_data:
      return

    if self.set_count == 1:
      index = self.iterator.next()

      self.current_data = self.selected_data[index]
      self.current_data['index'] = index
      self.current_data['order'] = self.iterator.count()
      print "Order: %s" % self.iterator.count()
    else:
      indexes = [self.iterator.next() for i in range(self.set_count)]
      self.current_data = [self.selected_data[idx] for idx in indexes]

      for idx in len(indexes):
        self.current_data[idx]['index'] = indexes[idx]
        self.current_data[idx]['order'] = self.iterator.count() + idx

  def select_iterator(self):
    self.order = self.sub_data.get('order', 'sequential')
    self.iterator = None

    for iterator in DataIterationMixin.iterators:
      if iterator.is_type(self.order):
        self.iterator = iterator(self.order)
        print "(%s) Iterator: %s" % (self.name, iterator.type())
        break

    if self.iterator is None:
      print 'Invalid ORDER (%s) specified in %s %s' % (self.order, self.parent.name, self.name)
      self.iterator = SequentialIterator(self.order)

    self.data_len = len(self.selected_data)
    self.iterator.set_range(0, self.iter_count)

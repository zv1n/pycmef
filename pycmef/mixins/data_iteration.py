#!/usr/bin/env python

import sys, json, os

from pycmef.iterators import *

class DataIterationMixin:
  iteration = 0
  def configure_iterations(self):
    self.iter_count = self.sub_data.get('iterations', 1)
    self.set_count = self.sub_data.get('sets', 1)

    self.this_set = self.sub_data.get('data', None)
    self.selected_data = self.parent.data.get_set(self.this_set)
    self.select_iterator()
    self.iteration = 0

  def data_to_json(self):
    return json.dumps(self.current_data)

  def should_repeat(self):
    return (self.iter_count == self.iteration) and (not self.iterator.done())

  def next(self):
    self.iteration += 1
    try:
      self.load_data()
      return True
    except KeyError, IndexError:
      return False

  def load_data(self):
    if self.set_count == 1:
      try:
        self.current_data = self.selected_data[self.iterator.next()]
      except IndexError as e:
        print e
    else:
      indexes = [self.iterator.next() for i in range(self.set_count)]
      self.current_data = [self.selected_data[idx] for idx in indexes]

  def select_iterator(self):
    self.order = self.sub_data.get('order', 'sequential')
    self.iterator = {
      'sequential': SequentialIterator(),
      'exclusive': RandomIterator()
    }[self.order]

    self.data_len = len(self.selected_data)
    self.iterator.set_range(0, self.data_len)

    self.next()

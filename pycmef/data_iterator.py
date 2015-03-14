#!/usr/bin/env python

import sys, json, os

from pycmef.iterators import *

class DataIterator:
  iterators = [
    SequentialIterator,
    RandomIterator,
    RandomGroup
  ]

  def __init__(self, sub, sets = 1, iterations = 1, order = None,
               dataset = None, data = None ):
    self.subsection = sub
    self.sets = sets
    self.order = order
    self.dataset = dataset
    self.data_list = data

    self.select_iterator(iterations, sets)

  def data_to_json(self):
    try:
      return json.dumps(self.current_data)
    except AttributeError:
      return '{}'

  def data_list_to_json(self):
    try:
      return json.dumps(self.data_list)
    except AttributeError:
      return '{}'

  def next(self):
    if self.data_list is None:
      self.current_data = None
      return False

    try:
      self.load_data()
      return True
    except KeyError, IndexError:
      return False

  def done(self):
    return self.iterator.done()

  def load_data(self):
    if not self.data_list:
      print "No data list."
      return

    if self.sets == 1:
      index = self.iterator.next()

      self.current_data = self.data_list[index]
      self.current_data['index'] = index
      self.current_data['order'] = self.iterator.count()
      print "Order: %s" % self.iterator.count()
      print "Index: %s" % index

    else:
      indexes = [self.iterator.next() for i in range(self.sets)]
      self.current_data = [self.data_list[idx] for idx in indexes]

      for idx in range(len(indexes)):
        self.current_data[idx]['index'] = indexes[idx]
        self.current_data[idx]['order'] = self.iterator.count() + idx

        print "Order(%s): %s" % (idx, self.iterator.count() + idx)
        print "Index(%s): %s" % (idx, indexes[idx])

  def select_iterator(self, iterations, sets):
    self.iterator = None

    for iterator in DataIterator.iterators:
      if iterator.is_type(self.order):
        self.iterator = iterator(self.order)
        print "(%s) Iterator: %s" % (self.subsection.name, iterator.type())
        break

    if self.iterator is None:
      print 'Invalid ORDER (%s) specified in %s %s' % (self.order, self.subsection.parent.name, self.subsection.name)
      self.iterator = SequentialIterator(self.order)

    self.data_len = len(self.data_list)
    print iterations
    print sets
    self.iterator.set_range(0, iterations * sets)

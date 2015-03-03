#!/usr/bin/env python

import sys, json, os

from pycmef.data_iterator import DataIterator

class DataIterationMixin:

  def data_to_json(self):
    try:
      if isinstance(self.selected_data, dict):
        data_dict = dict()

        for key in self.selected_data:
          data_dict[key] = self.selected_data[key].current_data

        return json.dumps(data_dict)
      else:
        return self.selected_data.data_to_json()
    except AttributeError:
      return '{}'

  def dataset_to_json(self):
    try:
      if isinstance(self.selected_data, dict):
        data_dict = dict()

        for key in self.selected_data:
          data_dict[key] = self.selected_data[key].data_list

        return json.dumps(data_dict)
      else:
        return self.selected_data.data_list_to_json()
    except AttributeError:
      return '{}'

  def next(self):
    self.iteration += 1

    if self.selected_data is None:
      return False

    if isinstance(self.selected_data, dict):
      for key in self.selected_data:
        self.selected_data[key].next()
    else:
      self.selected_data.next()

  def should_repeat(self):
    print "MAX: %s CUR: %s" % (self.iterations, self.iteration)
    return (self.iterations > self.iteration) and (not self.data_iterators_done())

  def data_iterators_done(self):
    if isinstance(self.selected_data, dict):
      done = False

      for key in self.selected_data:
        done = done or self.selected_data[key].done()

      return done
    else:
      return self.selected_data.done()

  def get_data(self, data_dict):
    return data_dict.get('data', None)

  def get_set_count(self, data_dict):
    return data_dict.get('sets', 1)

  def get_order(self, data_dict):
    return data_dict.get('order', 'sequential')

  def get_iteration_count(self, data_dict):
    return data_dict.get('iterations', None)

  def create_from_single_dataset(self, data_dict):
    dataset = self.get_data(data_dict)
    order = self.get_order(data_dict)
    sets = self.get_set_count(data_dict)
    contents = self.parent.data.get_set(dataset)

    self.set_default_iterations(contents)

    return DataIterator(self, sets = sets, iterations = self.iterations,
                        order = order, dataset = dataset,
                        data = contents)

  def create_from_multiple_datasets(self, sub_data):
    self.selected_data = dict()

    for key in sub_data:
      data_dict = sub_data[key]

      self.selected_data[key] = self.create_from_single_dataset(data_dict)

  def set_default_iterations(self, contents):
    if self.iterations is None:
      if contents is not None and isinstance(contents, list):
        self.iterations = len(contents)

    if self.iterations is None:
      self.iterations = 1

  def configure(self):
    self.iteration = -1
    self.iterations = self.get_iteration_count(self.sub_data)

    data = self.get_data(self.sub_data)

    if isinstance(data, str) or isinstance(data, unicode):
      self.selected_data = self.create_from_single_dataset(self.sub_data)
    elif isinstance(data, dict):
      self.selected_data = self.create_from_multiple_datasets(data)



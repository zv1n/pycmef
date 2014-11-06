
import sys

from pycmef.data_set import DataSet

class DataManagerMixin:
  def json_for_data_set(self, name):
    if self.data_dict is None:
      return {}
    return self.data_dict.to_json(name)

  def print_data(self):
    self.data_dict.print_stats()

  def process_data_set(self):
    try:
      self.data_dict = DataSet(self.data['data'])
    except KeyError:
      print u'Experiment does not contain a dataset.'
      self.data_dict = None

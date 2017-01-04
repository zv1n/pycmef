
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
    self.data_dict = DataSet(self.data.get('data', None))

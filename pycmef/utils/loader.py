
import os.path
import json

from yaml import safe_load

"""
  Load the experiment information from the JSON/YAML files.
"""
class ExperimentLoader:
  def __init__(self, exp):
    self.exp = exp
    self.load(exp.file)
    self.process_config()

  def process_config(self):
    self.core()

  def core(self):
    self.exp.data = self.exp_data
    self.exp.name = self.exp_data.get('experiment', 'Unnamed')
    self.exp.fullscreen = self.exp_data.get('fullscreen', False)

    try:
      self.exp.sections = self.exp_data['sections']
    except KeyError:
      raise Exception('Experiment must contain at least 1 section.')

  def sections(self):
    return

  # Helpers to load the experiment File
  def load(self, file):
    if not os.path.isfile(file):
      raise Exception(u"Experiment file must exist.")
    ext = os.path.splitext(file)[1]

    if ext == '.json':
      self.load_json(file)
    elif (ext == '.yaml') or (ext == '.yml'):
      self.load_yaml(file)

  def load_yaml(self, file):
    fh = open(file, 'r')
    self.exp_data = yaml.safe_load(file)
    fh.close()

  def load_json(self, file):
    fh = open(file, 'r')
    self.exp_data = json.load(fh)
    fh.close()
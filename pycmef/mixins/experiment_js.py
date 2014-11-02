#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import json

"""
  Handles attachment of Experiment JS connectors.
"""
class ExperimentJSMixin(QObject):
  @pyqtSlot(str)
  def next(self, msg):
    print(msg)

  # Entire experiment data file.
  def experiment_json(self):  
    return json.dumps(self.data)

  experiment = pyqtProperty(str, fget=experiment_json)

  # Entire dataset (post-processed).
  def dataset_json(self):  
    return self.dataset.to_json()

  _dataset = pyqtProperty(str, fget=dataset_json)

  # Current data field
  def subsection_json(self):  
    return self.subsection.to_json()

  _current = pyqtProperty(str, fget=subsection_json)

  def register_connectors(self, browser):
    browser.setJsObject('_experiment', self)

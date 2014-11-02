#!/usr/bin/env python

"""
  Experiment class handles loading the Experiment file and generating all
  necessary experiment components.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import sys

from pycmef.utils.loader import ExperimentLoader
from pycmef.utils.browser import EnhancedBrowser
from pycmef.mixins.experiment_js import ExperimentJSMixin

"""
  Handles the experiment setup based on input in the configuration.
"""
class Experiment(ExperimentJSMixin):
  # Create init files for 
  def __init__(self, file):
    super(Experiment, self).__init__()

    self.file = file
    ExperimentLoader(self)

  def run(self):
    self.app = QApplication(sys.argv)

    self.web = EnhancedBrowser()
    self.web.load(QUrl("./test.html"))
    self.register_connectors(self.web)

    if self.fullscreen:
      self.web.showMaximized()
    else:
      self.web.show()

    return self.app.exec_()

if __name__ == "__main__":
  import sys
  Experiment(sys.argv[1])
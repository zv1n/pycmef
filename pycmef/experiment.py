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

"""
  Handles the experiment setup based on input in the configuration.
"""
class Experiment(QObject):
  @pyqtSlot(str)
  def next(self, msg):
    print(msg)

  def _ExperimentJSON(self):  
    return json.dump(self.data)

  _experiment = pyqtProperty(str, fget=_ExperimentJSON)

  # Create init files for 
  def __init__(self, file):
    super(Experiment, self).__init__()

    self.file = file
    ExperimentLoader(self)

  def run(self):
    self.app = QApplication(sys.argv)

    self.web = EnhancedBrowser()
    self.web.load(QUrl("./test.html"))

    if self.fullscreen:
      self.web.showMaximized()
    else:
      self.web.show()

    return self.app.exec_()

if __name__ == "__main__":
  import sys
  Experiment(sys.argv[1])
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
from pycmef.mixins.event_manager import EventManagerMixin
from pycmef.mixins.section_manager import SectionManagerMixin
from pycmef.mixins.runner import RunnerMixin

from pycmef.event_handler import EventHandler

"""
  Handles the experiment setup based on input in the configuration.
"""
class Experiment(
  ExperimentJSMixin,
  EventManagerMixin,
  SectionManagerMixin,
  EventHandler,
  RunnerMixin):

  # Create init files for 
  def __init__(self, file):
    super(Experiment, self).__init__()
    self.file = file
    ExperimentLoader(self)

    self.register_runner_events()

  def run(self):
    self.app = QApplication(sys.argv)

    self.web = EnhancedBrowser()
    self.register_connectors()

    self.web.load(QUrl("./test.html"))

    if self.fullscreen:
      self.web.showMaximized()
    else:
      self.web.show()

    return self.app.exec_()

if __name__ == "__main__":
  import sys
  Experiment(sys.argv[1])
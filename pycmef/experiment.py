#!/usr/bin/env python

"""
  Experiment class handles loading the Experiment file and generating all
  necessary experiment components.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import sys, os

from pycmef.utils.loader import ExperimentLoader
from pycmef.utils.browser import EnhancedBrowser

from pycmef.mixins.experiment_js import ExperimentJSMixin
from pycmef.mixins.event_manager import EventManagerMixin
from pycmef.mixins.section_manager import SectionManagerMixin
from pycmef.mixins.data_manager import DataManagerMixin
from pycmef.mixins.runner import RunnerMixin
from pycmef.mixins.response import ResponseMixin

from pycmef.event_handler import EventHandler

if "--pygaze" in sys.argv:
  from pycmef.pygaze_eyetracker import PygazeEyetracker

"""
  Handles the experiment setup based on input in the configuration.
"""
class Experiment(
  ExperimentJSMixin,
  EventManagerMixin,
  SectionManagerMixin,
  DataManagerMixin,
  ResponseMixin,
  RunnerMixin,
  EventHandler):

  # Create init files for 
  def __init__(self, file):
    super(Experiment, self).__init__()
    self.file = file
    self.directory = os.path.dirname(file)

    ExperimentLoader(self)

    self.register_runner_events()
    self.init_response()

    # Try to instantiate PygazeEyetracker if the class exists.
    # Ignore the error if it doesn't.
    try:
      self.eyetracker = PygazeEyetracker()
      self.eyetracker.register(self)
    except NameError:
      pass

  def load_page(self, page):
    # print "Loading page: %s" % page
    self.web.load(QUrl(QString(page)))

  def run(self):
    self.app = QApplication(sys.argv)

    self.web = EnhancedBrowser()
    self.register_connectors()

    self.web.load(QUrl("./cmef/selftest.html"))

    if self.fullscreen:
      self.web.showMaximized()
    else:
      self.web.show()

    return self.app.exec_()

if __name__ == "__main__":
  import sys
  Experiment(sys.argv[1])
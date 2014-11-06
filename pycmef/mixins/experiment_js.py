#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import json

"""
  Handles attachment of Experiment JS connectors.
"""
class ExperimentJSMixin(QObject):

  @pyqtSlot(str, str)
  def emit(self, qevent, qargs):
    event = unicode(qevent)
    args = unicode(qargs)

    if len(args) > 1:
      try:
        args = json.loads(args)
      except ValueError:
        pass

    result = self.handle_event(event, args)
    self.on_event_response.emit(event, result)

  # Entire experiment data file.
  def experiment_json(self):  
    return json.dumps(self.data)

  # Entire dataset (post-processed).
  def dataset_json(self):  
    return self.data_dict.to_json()

  # Current data field
  def subsection_json(self):  
    return self.current_subsection.to_json()

  on_event_response = pyqtSignal(str, str)

  experiment = pyqtProperty(str, fget=experiment_json)
  dataset = pyqtProperty(str, fget=dataset_json)
  subsection = pyqtProperty(str, fget=subsection_json)

  def register_connectors(self):
    self.html_view().loadFinished.connect(self.on_load)

  def html_view(self):
    if isinstance(self.web, QWebView):
      return self.web
    else:
      return self.web.html_view

  def on_load(self):
    page = self.html_view().page()
    page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

    main_frame = page.mainFrame()
    main_frame.addToJavaScriptWindowObject("_experiment", self)
    main_frame.evaluateJavaScript("on_python_ready()")
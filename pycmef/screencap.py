
from pycmef.event_handler import returns_string, returns_dictionary
from PyQt4.QtGui import * 

import os
import sys

class ScreenCapHandler:
  def __init__(self):
    pass

  def register(self, experiment):
    experiment.register_events({
      'screen_capture': self.capture
    })

    self.experiment = experiment

  @returns_string
  def capture(self, args):
    name = args.get('name', None)

    filename = "p%s_%s_%s_%s" % (
      self.experiment.participant,
      self.experiment.current_section.name,
      self.experiment.current_subsection.name,
      self.experiment.current_subsection.iteration - 1)

    if not name is None:
      filename = "%s_%s" % (filename, name)

    filename = "%s.png" % filename

    file_path = os.path.join(self.experiment.output_path, filename)

    QPixmap.grabWindow(
      QApplication.desktop().winId(),0,0,
      QApplication.desktop().screenGeometry().width(),
      QApplication.desktop().screenGeometry().height()).save(file_path)

    return str(filename)

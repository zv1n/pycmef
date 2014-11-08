
import sys, os

from pycmef.event_handler import returns_string, returns_dictionary

class PygazeEyetracker:
  def register(self, event_manager):
    event_manager.register_events({
      'calibrate_eyetracker': self.calibrate_eyetracker,
      'start_tracking': self.start_tracking,
      'stop_tracking': self.stop_tracking,
      'log_to_eyetracker': self.log_to_eyetracker
    })

  @returns_string
  def calibrate_eyetracker(self, args):
    return ""

  @returns_string
  def start_tracking(self, args):
    return ""

  @returns_string
  def stop_tracking(self, args):
    return ""

  @returns_string
  def log_to_eyetracker(self, args):
    return ""
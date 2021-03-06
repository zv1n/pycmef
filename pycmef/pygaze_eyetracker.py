
import sys, os, random, constants

from pycmef.event_handler import returns_string, returns_dictionary

from pygaze import libscreen
from pygaze import libtime
from pygaze import liblog
from pygaze import libinput
from pygaze import eyetracker


class PygazeEyetracker:
  def __init__(self):
    # create display object
    self.disp = libscreen.Display()

    # create eyetracker object
    self.tracker = eyetracker.EyeTracker(self.disp)

    # create keyboard object
    self.keyboard = libinput.Keyboard(keylist=['space'], timeout=None)

    # create logfile object
    self.log = liblog.Logfile()

  def register(self, event_manager):
    event_manager.register_events({
      'calibrate_eyetracker': self.calibrate_eyetracker,
      'start_eyetracker': self.start_tracking,
      'stop_eyetracker': self.stop_tracking,
      'log_to_eyetracker': self.log_to_eyetracker
    })

  @returns_string
  def calibrate_eyetracker(self, args):
    # calibrate eye tracker
    self.tracker.calibrate()
    return ""

  @returns_string
  def start_tracking(self, args):
    self.tracker.start_recording()
    return ""

  @returns_string
  def stop_tracking(self, args):
    self.tracker.stop_recording()
    return ""

  @returns_string
  def log_to_eyetracker(self, args):
    self.tracker.log(args.message)
    return ""



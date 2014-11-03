
import sys, os

from pycmef.event_handler import returns_string, returns_dictionary

class RunnerMixin:
  def register_runner_events(self):
    self.register_events({
      'next': self.next_event,
      'refresh': self.refresh_event,
      'check': self.check_event,
      'show': self.show_event
    })

  @returns_dictionary
  def show_event(self, args):
    return {}

  @returns_string
  def next_event(self, args):
    pass

  @returns_string
  def refresh_event(self, args):
    pass

  @returns_dictionary
  def check_event(self, args):
    pass
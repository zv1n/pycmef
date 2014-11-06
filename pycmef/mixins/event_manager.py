#!/usr/bin/env python

import json

"""
  Handles events passed from the ThinClient
"""
class EventManagerMixin(object):
  def configure(self):
    try:
      getattr(self, '__event_handlers__')         
      return True
    except AttributeError:
      self.__event_handlers__ = {}
      return False

  def get_event_handler(self, event):
    if not self.configure():
      return None

    return self.__event_handlers__.get(event, None)

  def handle_event(self, event, args):
    event = self.get_event_handler(event)

    if event is None:
      print 'No handler registered.'
      return '$ERROR:no_event_handler'

    return event(args)

  def register_event(self, event, method):
    self.configure()

    if event in self.__event_handlers__:
      raise Exception("Even %s is already registered!" % event)

    self.__event_handlers__[event] = method

  def register_events(self, events):
    for event in events:
      self.register_event(event, events[event])

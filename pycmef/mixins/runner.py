
import sys, os
import datetime

from pycmef.event_handler import returns_string, returns_dictionary

class RunnerMixin:
  def register_runner_events(self):
    self.register_events({
      'start': self.start_event,
      'next': self.next_event,
      'refresh': self.refresh_event,
      'check': self.check_event,
      'show': self.show_event
    })

  @returns_dictionary
  def show_event(self, args):
    return {}

  @returns_string
  def start_event(self, args):
    self.participant = args['participant']
    self.condition = args.get('condition', None)
    self.add_core_response(args)

    self.data_dict.set_condition(self.condition)
    self.configure_sections()

    self.load_page(self.current_subsection.path(self.directory))
    return 'success'

  def load_conclusion(self):
    self.load_page('./cmef/conclusion.html')
    return 'end'

  @returns_string
  def next_event(self, args):
    if self.current_subsection is None:
      return self.load_conclusion()

    self.add_response(args)

    self.next_subsection()

    if self.current_subsection is None:
      return self.load_conclusion()

    # print "%s:%s" % (self.current_section.name, self.current_subsection.name)
    self.load_page(self.current_subsection.path(self.directory))
    return 'success'

  @returns_string
  def refresh_event(self, args):
    pass

  @returns_dictionary
  def check_event(self, args):
    pass
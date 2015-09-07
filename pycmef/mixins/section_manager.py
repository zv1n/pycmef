
import sys

from pycmef.section import Section

class SectionManagerMixin:
  def init_section_manager(self):
    self.initialized = False
    self.current_section = None
    self.current_subsection = None

  def json_for_section(self, name):
    for sect in self.sections:
      if sect.name == name:
        return sect

    return None

  def print_sections(self):
    for sect in self.sections:
      print "Section: %s" % sect.name
      sect.print_section()

  def configure_sections(self):
    for section in self.sections:
      section.configure_subsections()

    self.update_current_section()
    self.initialized = True

  def process_sections(self):
    try:
      self.sections = [Section(sec, self) for sec in self.data['sections']]
    except KeyError:
      raise Exception('Experiment must contain at least 1 section.')

    self.current_section_index = 0

  def update_current_section(self):
    try:
      self.current_section = self.sections[self.current_section_index]
      self.current_subsection = self.current_section.next_subsection()
    except IndexError:
      self.current_section = self.current_subsection = None

  def next_subsection(self):
    if self.current_section is None:
      return None

    self.current_subsection = self.current_section.next_subsection()

    if self.current_subsection is None:
      self.current_section_index += 1
      self.update_current_section()

    return self.current_subsection



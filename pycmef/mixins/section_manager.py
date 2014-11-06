
import sys

from pycmef.section import Section

class SectionManagerMixin:
  def json_for_section(self, name):
    for sect in self.sections:
      if sect.name == name:
        return sect

    return None

  def print_sections(self):
    for sect in self.sections:
      print "Section: %s" % sect.name
      sect.print_section()

  def process_sections(self):
    try:
      self.sections = [Section(sec, self) for sec in self.data['sections']]
    except KeyError:
      raise Exception('Experiment must contain at least 1 section.')

    self.current_section_index = 0
    self.update_current_section()

  def update_current_section(self):
    self.current_section = self.sections[self.current_section_index]
    self.current_subsection = self.current_section.current_subsection

  def next_subsection(self):
    self.current_subsection = self.current_section.next_subsection()

    if self.current_subsection is None:
      self.current_section_index += 1
      self.update_current_section()

    return self.current_subsection



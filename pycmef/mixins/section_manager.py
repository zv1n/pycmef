
import sys

from pycmef.section import Section

class SectionManagerMixin:
  def json_for_section(self, name):
    for sect in self.sections:
      if sect.name == name:
        return sect

    return None

  def process_sections(self):
    try:
      self.sections = [Section(sec, self) for sec in self.data['sections']]
    except KeyError:
      raise Exception('Experiment must contain at least 1 section.')
#!/usr/bin/env python

import sys, json

from pycmef.subsection import Subsection

class Section:
  def __init__(self, section, parent):
    self.parent = parent
    self.data = parent.data_dict

    if not isinstance(section, dict):
      raise Exception("Section must be an Dictionary!")
    
    self.section_data = section

    try:
      self.name = section['name']
    except:
      raise Exception("Every section must contain a name!")

    self.process_subsections()

  def print_section(self):
    print "Subsection: %s" % ', '.join([sub.name for sub in self.subsections])

  def configure_subsections(self):
    for subsection in self.subsections:
      subsection.configure()

  def process_subsections(self):
    try:
      subsections = self.section_data['subsections']
    except KeyError:
      raise Exception('Every section must contain at least 1 subsection.')

    self.subsections = [Subsection(sub, self) for sub in subsections]

    self.current_subsection_index = 0
    self.update_current_subsection()

  def update_current_subsection(self):
    self.current_subsection = self.subsections[self.current_subsection_index]
    if self.current_subsection is None:
      print "Current Sub: %s" % self.current_subsection.name

  def next_subsection(self):
    if self.current_subsection.should_repeat():
      self.current_subsection.next()
      return self.current_subsection
    else:
      self.current_subsection_index += 1
      try:
        self.current_subsection = self.subsections[self.current_subsection_index]
        return self.current_subsection
      except IndexError:
        return None

  def to_json(self):
    return json.dumps(self.section_data)

if __name__ == "__main__":
  import sys
  with open(sys.argv[1], 'r') as file:
    print Section(file.read()).to_json()
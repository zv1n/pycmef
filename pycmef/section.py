#!/usr/bin/env python

import sys, json

from pycmef.subsection import Subsection

class Section:
  def __init__(self, section, parent):
    self.parent = parent

    if not isinstance(section, dict):
      raise Exception("Section must be an Dictionary!")
    
    self.section_data = section

    try:
      self.name = section['name']
    except:
      raise Exception("Every section must contain a name!")

    self.process_subsections()

  def process_subsections(self):
    try:
      subsections = self.section_data['subsections']
    except KeyError:
      raise Exception('Every section must contain at least 1 subsection.')

    self.subsections = [Subsection(sub, self) for sub in subsections]

  def to_json(self):
    return json.dumps(self.section_data)

if __name__ == "__main__":
  import sys
  with open(sys.argv[1], 'r') as file:
    print Section(file.read()).to_json()
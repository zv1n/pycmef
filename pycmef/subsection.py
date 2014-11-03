#!/usr/bin/env python

import sys, json

class Subsection: 
  def __init__(self, sub, parent):
    self.parent = parent

    if isinstance(sub, dict):
      self.sub_data = sub
    elif isinstance(sub, str) or isinstance(sub, unicode):
      self.sub_data = { 'name': sub }

    try:
      self.name = self.sub_data['name']
    except:
      raise Exception("All subsections in %s must contain a name!" % parent.name)

  def to_json(self):
    return json.dumps(self.section_data)

if __name__ == "__main__":
  import sys
  with open(sys.argv[1], 'r') as file:
    print Subsection(file.read()).to_json()
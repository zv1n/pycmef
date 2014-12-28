#!/usr/bin/env python

import sys, json, os

from pycmef.mixins.data_iteration import DataIterationMixin

class Subsection(DataIterationMixin): 
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

  def path(self, relative = '.'):
    abs_html = '/'.join([self.parent.name, self.name])
    html = '/'.join([relative, self.parent.name, self.name])
    if os.path.exists(html + '.html'):
      return html + '.html'
    if os.path.exists(html + '.htm'):
      return html + '.htm'
    if os.path.exists(abs_html + '.html'):
      return html + '.html'
    if os.path.exists(abs_html + '.htm'):
      return html + '.htm'
    return u'./cmef/end.html'

  def to_json(self):
    return json.dumps(self.sub_data)

if __name__ == "__main__":
  import sys
  with open(sys.argv[1], 'r') as file:
    print Subsection(file.read()).to_json()
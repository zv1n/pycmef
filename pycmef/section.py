#!/usr/bin/env python

import sys

from pycmef.utils.loader import ExperimentLoader
from pycmef.utils.browser import EnhancedBrowser

class Section: 
  def __init__(self, dict):
    return

if __name__ == "__main__":
  import sys
  with open(sys.argv[1], 'r') as file:
    print Session(file.read()).to_json()
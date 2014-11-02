#!/usr/bin/env python

import sys

from pycmef.experiment import Experiment

if (len(sys.argv) != 2):
  print('usage: cmef.py <experiment json or yml>')
  sys.exit(1)

exp = Experiment('experiment.json')
result = exp.run()

sys.exit(result)


#!/usr/bin/env python

import sys

from pycmef.experiment import Experiment

exp = Experiment('experiment.json')
result = exp.run()

sys.exit(result)


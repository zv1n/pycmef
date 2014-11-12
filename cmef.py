#!/usr/bin/env python

import sys
import glob
import os

from subprocess import call

from pycmef.experiment import Experiment
from pycmef.screencap import ScreenCapHandler
from pycmef.event_handler import *

if "--pygaze" in sys.argv:
  from pycmef.pygaze_eyetracker import PygazeEyetracker
  load_pygaze = True
else:
  load_pygaze = False

if "--debug" in sys.argv:
  debug = True
else:
  debug = False



def usage():
  print('usage: cmef.py <experiment json or yml or directory>')
  sys.exit(1)

def copy_dependencies(directory):
  call(['cp', '-r', './cmef', directory])

def main():
  if (len(sys.argv) <= 1):
    usage()

  experiment = sys.argv[1]

  if os.path.isdir(experiment):
    try:
      config = glob.glob("%s/*.json" % experiment).pop()
    except IndexError:
      raise Exception("Unable to find experiment file in directory: %s" %
        experiment)
  elif not os.path.exists(experiment):
    raise Exception("Unable to find experiment file or directory: %s" %
      experiment)
  else:
    config = experiment

  copy_dependencies(os.path.dirname(config))

  exp = Experiment(config)
  exp.set_debug(debug)

  cap = ScreenCapHandler()
  cap.register(exp)

  # Try to instantiate PygazeEyetracker if the class exists.
  # Ignore the error if it doesn't.
  if load_pygaze:
    eyetracker = PygazeEyetracker()
    eyetracker.register(exp)

  result = exp.run()
  sys.exit(result)

if __name__ == '__main__':
  # try:
  main()
  # except Exception as e:
  #   print str(e)
  #   usage()
  #   sys.exit(1)
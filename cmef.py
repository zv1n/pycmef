#!/usr/bin/env python

import sys
import glob
import os
import shutil
import getopt

from pycmef.experiment import Experiment
from pycmef.screencap import ScreenCapHandler
from pycmef.event_handler import *

def usage(error = None):
  if error is not None:
    print(error)
  print('usage: cmef.py [-hdp] -e <experiment dir> -o <output dir>')
  sys.exit(1)

def copy_dependencies(directory):
  if os.name != 'posix':
    return
  dest = os.path.join(directory, 'cmef')
  if os.path.exists(dest):
    shutil.rmtree(dest)
  shutil.copytree('./cmef', dest)

def main(argv):
  if (len(argv) <= 1):
    usage('Not enough arguments provided.')

  try:
    long_form = ["help", "experiment=", "output=", "pygaze", "audio", "debug"]
    opts, args = getopt.getopt(argv[1:], "he:o:pad", long_form)
  except getopt.GetoptError as error:
    usage(str(error))
    sys.exit(2)

  load_pygaze = False
  debug = False
  experiment = None
  output_directory = None

  for opt, arg in opts:
    if opt in ("-d", "--debug"):
      debug = True

    elif opt in ("-h", "--help"):
      usage()
      sys.exit(1)

    elif opt in ("-p", "--pygaze"):
      from pycmef.pygaze_eyetracker import PygazeEyetracker
      load_pygaze = True

    elif opt in ("-a", "--audio"):
      from pycmef.pyaudio_handler import PyAudioHandler
      load_pyaudio = True

    elif opt in ("-e", "--experiment="):
      experiment = arg

    elif opt in ("-o", "--output="):
      output_directory = arg

  if experiment is None or output_directory is None:
    usage('Experiment or Output directory was not found.')
    sys.exit(1)

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

  if not os.path.isdir(output_directory):
    usage('Provided output directory is not a directory!')
    sys.exit(1)

  copy_dependencies(os.path.dirname(config))

  exp = Experiment(config, output_directory)
  exp.set_debug(debug)

  cap = ScreenCapHandler()
  cap.register(exp)

  # Try to instantiate PygazeEyetracker if the class exists.
  # Ignore the error if it doesn't.
  if load_pygaze:
    eyetracker = PygazeEyetracker()
    eyetracker.register(exp)

  # Try to instantiate PyAudioHandler if the class exists.
  # Ignore the error if it doesn't.
  if load_pyaudio:
    audio = PyAudioHandler()
    audio.register(exp)

  result = exp.run()
  sys.exit(result)

if __name__ == '__main__':
  # try:
  main(sys.argv)
  # except Exception as e:
  #   print str(e)
  #   usage()
  #   sys.exit(1)
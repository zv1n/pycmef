#!/usr/bin/env python

import sys
import getopt
import os
import csv
import glob

from cmef_parser import generate_output_file, load_experiment
from cmef_analyze_images import fetch_and_process_images

from subprocess import call

def usage(error = None):
  if error is not None:
    print error
  print('output parser:')
  print('usage: cmef-parse-all.py -d <parser-files dir> -o <test output dir>\n')
  print('image parser:')
  print('usage: cmef-parse-all.py -s preferences.preferences[,performance.question[,...]] ')
  print('                         -o <test output dir>')
  sys.exit(1)

def fetch_json(dir, deep):
  if deep:
    return glob.glob(os.path.join(dir, '**', '*.json'))
  else:
    return glob.glob(os.path.join(dir, '*.json'))

def run_parser(experiment, definition):
  outputdir = os.path.dirname(experiment)
  basename = os.path.basename(definition)
  csv = "%s.csv" % os.path.splitext(basename)[0]
  output = os.path.join(outputdir, csv)

  print "Generating output: %s for %s" % (csv, experiment)
  generate_output_file(experiment, definition, output)

def run_image_analysis(exp, sections, plot):
  expc = load_experiment(exp)
  outputdir = os.path.dirname(exp)
  plotdir = os.path.join(outputdir, plot)
  part = expc['participant']
  events = os.path.join(outputdir, "%s Events.txt" % part)

  fetch_and_process_images(expc, sections, events, outputdir, plotdir)

def main(argv):
  if (len(argv) <= 1):
    usage()

  try:
    long_form = ["help", "definitions=", "output=", "plot-dir=", "subsections="]
    opts, args = getopt.getopt(argv[1:], "hd:o:s:p:", long_form)
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  def_dir = None
  out_dir = None
  subsections = []
  definitions = []

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit(1)

    elif opt in ("-d", "--definitions="):
      def_dir = arg

    elif opt in ("-s", "--subsections="):
      subsections.extend(arg.split(','))

    elif opt in ("-o", "--output="):
      out_dir = arg

    elif opt in ("-p", "--plot-dir="):
      plot_dir = arg

  if def_dir is None and len(subsections) == 0:
    usage("No parser definition directory or subsections specified.")
    sys.exit(1)

  if out_dir is None:
    usage("No output directory specified.")
    sys.exit(1)

  if not os.path.isdir(out_dir):
    usage()
    sys.exit(1)

  if def_dir is not None:
    if not os.path.isdir(def_dir):
      usage()
      sys.exit(1)

    definitions = fetch_json(def_dir, False)

  if len(subsections) == 0 and len(definitions) == 0:
    usage("This script must be given subsections or a definitions directory for parsing.")
    sys.exit(1)

  outputs = fetch_json(out_dir, True)

  for exp in outputs:
    if len(definitions) > 0:
      for parserdef in definitions:
        run_parser(exp, parserdef)
    if len(subsections) > 0:
      run_image_analysis(exp, subsections, plot_dir)

if __name__ == '__main__':

  main(sys.argv)
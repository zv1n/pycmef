#!/usr/bin/env python

import sys
import getopt
import os
import csv
import glob

from cmef_parser import generate_output_file

from subprocess import call

def usage(error = None):
  if error is not None:
    print error
  print('usage: cmef-parse-all.py -d <parser-files dir> -o <test output dir> -e <exec command>')
  sys.exit(1)

def fetch_json(dir, deep):
  if deep:
    return glob.glob(os.path.join(dir, '**', '*.json'))
  else:
    return glob.glob(os.path.join(dir, '*.json'))

def run_parser(exec_command, experiment, definition):
  outputdir = os.path.dirname(experiment)
  basename = os.path.basename(definition)
  csv = "%s.csv" % os.path.splitext(basename)[0]
  output = os.path.join(outputdir, csv)

  print "Generating output: %s for %s" % (csv, experiment)
  generate_output_file(experiment, definition, output)

def main(argv):
  if (len(argv) <= 1):
    usage()

  try:
    long_form = ["help", "definitions=", "output="]
    opts, args = getopt.getopt(argv[1:], "hd:o:", long_form)
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  def_dir = None
  out_dir = None
  ecommand = None

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit(1)

    elif opt in ("-d", "--definitions="):
      def_dir = arg

    elif opt in ("-o", "--output="):
      out_dir = arg

  if def_dir is None:
    usage("No parser definition directory specified.")
    sys.exit(1)

  if out_dir is None:
    usage("No output directory specified.")
    sys.exit(1)

  if not os.path.isdir(def_dir) or not os.path.isdir(out_dir):
    usage()
    sys.exit(1)

  definitions = fetch_json(def_dir, False)
  outputs = fetch_json(out_dir, True)

  for exp in outputs:
    for parserdef in definitions:
      run_parser(ecommand, exp, parserdef)

if __name__ == '__main__':

  main(sys.argv)
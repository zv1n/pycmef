#!/usr/bin/env python

import sys
import getopt
import json
import os
import csv

def usage(error = None):
  if error is not None:
    print error
  print('usage: cmef-parser.py [-h] -c <config> -i <experiment output> -o <output file>')
  sys.exit(1)

class ConfigEngine:
  def __init__(self):
    self.experiment = None
    self.config = None

  def generate_path(self, item):
    if len(self.path) == 0:
      return str(item)

    return str("%s.%s" % (str.join('.', self.path), item))

  def generate_value(self, item):
    return item

  def nested_key(self, key, itm):
    if type(itm) is dict:
      keys = key.split('.')
      for key in keys:
        itm = itm.get(key, None)

        if type(itm) is dict:
          continue

        return itm
    else:
      return itm

  def generate_response(self, item):
    if len(self.path) == 0:
      return self.experiment.get(item, None)

    res = []

    env = self.experiment
    for idx in range(0, len(self.path)+1):
      try:
        key = self.path[idx]
      except IndexError:
        key = item

      if type(env) is list:
        for itm in env:
          res.append(self.nested_key(key, itm))
      elif type(env) is dict:
        env = env.get(key, None)
      elif type(env) is unicode:
        return env

    return res

  def parse_list(self, items, handler):
    line = []

    for item in items:
      res = None

      if type(item) is unicode:
        res = handler(item)
      elif type(item) is dict:
        res = self.parse_dict(item, handler)
      elif type(item) is list:
        res = self.parse_list(item, handler)

      if not res is None:
        line.append(res)

    return line

  def parse_dict(self, obj, handler):
    line = []

    for key in obj:
      self.path.append(key)
      item = obj[key]
      res = None

      if type(item) is unicode:
        res = handler(item)
      elif type(item) is dict:
        res = self.parse_dict(item, handler)
      elif type(item) is list:
        res = self.parse_list(item, handler)

      if not res is None:
        if type(res) is list:
          line.extend(res)
        else:
          line.append(res)

      self.path.pop()

    return line

  def process_config(self, handler):
    resp = []
    self.path = []

    for item in self.config:
      res = None

      if type(item) is unicode:
        res = handler(item)
      elif type(item) is dict:
        res = self.parse_dict(item, handler)

      if not res is None:
        if type(res) is list:
          resp.extend(res)
        else:
          resp.append(res)

    return resp

  def header(self):
    return self.process_config(self.generate_path)

  def row_count(self, res):
    maxr = 0
    for row in res:
      if type(row) is list:
        if len(row) > maxr:
          maxr = len(row)
    return maxr

  def response(self):
    res = self.process_config(self.generate_response)

    rows = self.row_count(res)
    nres = []

    """
      Currently, the response is in a list of columns...
      CSV writer wants list of rows.
    """
    for idx in range(0, rows):
      crow = []

      for row in res:
        if type(row) is unicode:
          crow.append(row)
        elif type(row) is list:
          if len(row) is 0:
            crow.append(None)
          else:
            crow.append(row.pop(0))

      nres.append(crow)

    return nres


def main(argv):
  if (len(argv) <= 1):
    usage("Invalid number of arguments.")

  try:
    long_form = ["help", "input=", "config=", "output="]
    opts, args = getopt.getopt(argv[1:], "hi:o:c:", long_form)
  except getopt.GetoptError as err:
    usage("Invalid option: %s" % err)
    sys.exit(2)

  input_file = None
  config_file = None
  output_file = None

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit(1)

    elif opt in ("-i", "--input="):
      input_file = arg

    elif opt in ("-c", "--config="):
      config_file = arg

    elif opt in ("-o", "--output="):
      output_file = arg

  if input_file is None or config_file is None or output_file is None:
    usage("No input/config/output file specified.")
    sys.exit(1)

  if not os.path.isfile(input_file) or not os.path.isfile(config_file):
    usage("Invalid input or configuration file path.")
    sys.exit(1)

  generate_output_file(input_file, config_file, output_file)

def generate_output_file(input_file, config_file, output_file):
  handle = open(input_file)
  experiment = json.load(handle)
  handle.close()

  handle = open(config_file)
  config = json.load(handle)
  handle.close()

  engine = ConfigEngine()
  engine.config = config
  engine.experiment = experiment

  headers = [engine.header()]
  response = engine.response()

  headers.extend(response)

  outfile = open(output_file, 'wb')
  csv_write = csv.writer(outfile, dialect = 'excel')
  csv_write.writerows(headers)
  outfile.close()

if __name__ == '__main__':

  main(sys.argv)
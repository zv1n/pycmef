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

def load_experiment(fle):
  with open(fle, 'rb') as jsonfile:
    return json.load(jsonfile)

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

  def nested_list_key(self, key, itms):
    res = []

    for itm in itms:
      kval = self.nested_key(key, itm)
      res.append(kval)

    return res

  def nested_key(self, key, itm):
    if type(itm) is dict:
      keys = key.split('.')
      for idx, key in enumerate(keys):
        if key[-2:] == '[]':
          itm = itm.get(key[:-2], None)
          kstr = ".".join(keys[idx+1:])

          return self.nested_list_key(kstr, itm)

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

  def max_per_row(self, res):
    exp = []
    for row in res:
      if type(row) is list:

        for idx, item in enumerate(row):
          if type(item) is list:

            while len(exp) <= idx:
              exp.append(len(item))

            if exp[idx] < len(item):
              exp[idx] = len(item)

    return exp

  def expanded_header(self, res, colmajor):
    hdr = self.header()

    if colmajor:
      return (hdr, self.max_per_row(res))

    expand = [1] * len(hdr)

    for idx, col_data in enumerate(res):
      if type(col_data) is not list:
        continue

      for ent in col_data:
        if type(ent) is not list:
          continue

        exp = expand[idx]
        if len(ent) > exp:
          expand[idx] = len(ent)

    updated_hdr = []
    for idx, cnt in enumerate(expand):
      itm = hdr[idx]
      if cnt > 0:
        inject = []
        for cnt in range(0, cnt):
          inject.append(itm.replace("[]", "[%s]" % cnt))

        updated_hdr.append(inject)
      else:
        updated_hdr.append(itm)

    return ([item for sl in updated_hdr for item in sl], expand)

  def response(self, colmajor):
    res = self.process_config(self.generate_response)

    rows = self.row_count(res)
    nres = []

    hdr, expanded = self.expanded_header(res, colmajor)

    """
      Currently, the response is in a list of columns...
      CSV writer wants list of rows.
    """
    for ridx in range(0, rows):
      crow = []

      for idx, row in enumerate(res):
        if type(row) is unicode:
          crow.append(row)

        elif type(row) is list:

          if len(row) is 0:
            crow.append(None)
          else:
            erow = row.pop(0)
            if erow is None:
              erow = []

            if colmajor:
              exp = expanded[ridx]

              if type(erow) is list and not colmajor:
                crow.extend([itm for itm in erow])
              else:
                crow.append(erow)
            else:
              exp = expanded[idx]

              for n in range(len(erow), exp):
                erow.append(None)

              if type(erow) is list and not colmajor:
                crow.extend([itm for itm in erow])
              else:
                crow.append(erow)

      for n in range(exp):
        if colmajor:
          temp = crow[:]

          for idx, row in enumerate(crow):
            if type(row) is list:
              temp[idx] = row[n]

          nres.append(temp)
        else:
          nres.append(crow)

    hres = [hdr]

    hres.extend(nres)
    return hres

def transpose(lol):
  if len(lol) == 0:
    return []
  rowlen = len(lol[0])
  out = []

  for i in range(rowlen):
    for l in lol:
      d = l[i]
      if len(out) <= i:
        out.append([d])
      else:
        out[i].append(d)

  return out

def main(argv):
  if (len(argv) <= 1):
    usage("Invalid number of arguments.")

  try:
    long_form = ["help", "input=", "config=", "output=", "tranpose", "row-major"]
    opts, args = getopt.getopt(argv[1:], "hi:o:c:tr", long_form)
  except getopt.GetoptError as err:
    usage("Invalid option: %s" % err)
    sys.exit(2)

  input_file = None
  config_file = None
  output_file = None
  trans = False
  colmajor = True

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

    elif opt in ("-t", "--transpose"):
      trans = True

    elif opt in ("-r", "--row-major"):
      colmajor = False

  if input_file is None or config_file is None or output_file is None:
    usage("No input/config/output file specified.")
    sys.exit(1)

  if not os.path.isfile(input_file) or not os.path.isfile(config_file):
    usage("Invalid input or configuration file path.")
    sys.exit(1)

  generate_output_file(input_file, config_file, output_file, trans, colmajor)

def generate_output_file(input_file, config_file, output_file, trans, colmajor):
  handle = open(input_file)
  experiment = json.load(handle)
  handle.close()

  handle = open(config_file)
  config = json.load(handle)
  handle.close()

  engine = ConfigEngine()
  engine.config = config
  engine.experiment = experiment

  headers = engine.response(colmajor)

  if trans:
    headers = transpose(headers)

  outfile = open(output_file, 'wb')
  csv_write = csv.writer(outfile, dialect = 'excel')
  csv_write.writerows(headers)
  outfile.close()

if __name__ == '__main__':

  main(sys.argv)
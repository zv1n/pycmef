#!/usr/bin/env python
# analysis script for natural viewing experiment
#
# version 1 (27 May 2015)

__author__ = "Terry Meacham"

# native
import os

# custom
from pygazeanalyser.smireader import read_smioutput, SMIModes
from pygazeanalyser.gazeplotter import draw_fixations, draw_heatmap, draw_scanpath, draw_raw

# external
import numpy

import sys
import json

def get_screencaps(exp, components):
  top = exp
  for comp in components:
    top = top.get(comp, None)
    if top is None:
      raise Exception("Unable to find response item: %s" % ".".join(components))

  flist = []
  for item in top:
    scaps = item.get('screencap', ['No Screencaps'])
    flist.append(scaps[0])

  return flist


def get_file_list(fle, components):
  with open(fle, 'rb') as jsonfile:
    exp = json.load(jsonfile)
    files = []

    for comp in components:
      flist = get_screencaps(exp, comp.split('.'))
      files.extend(flist)

  return files

def load_experiment(fle):
  with open(fle, 'rb') as jsonfile:
    return json.load(jsonfile)

def get_file_list(exp, components):
  files = []

  for comp in components:
    flist = get_screencaps(exp, comp.split('.'))
    files.extend(flist)

  return files

def process_images(imglist, eventfile, ppname, imgdir, plotdir):

  # check if the image directory exists
  if not os.path.isdir(imgdir):
    raise Exception("ERROR: no image directory found; path '%s' does not exist!" % imgdir)

  # check if output directorie exist; if not, create it
  if not os.path.isdir(plotdir):
    os.mkdir(plotdir)

  # EXPERIMENT SPECS
  DISPSIZE = (1920,1080) # (px,px)
  SCREENSIZE = (39.9,29.9) # (cm,cm)
  SCREENDIST = 61.0 # cm
  PXPERCM = numpy.mean([DISPSIZE[0]/SCREENSIZE[0],DISPSIZE[1]/SCREENSIZE[1]]) # px/cm

  # read the file
  smidata = read_smioutput(eventfile, None, ag_mode=SMIModes.LEFT_ONLY, stop=None, debug=False)

  nokey = 0
  processed = 0

  # loop through trials
  for trialnr in range(len(imglist)):
    # load image name, saccades, and fixations
    imgname = imglist[int(trialnr)]
    try:
      saccades = smidata[trialnr]['events']['Esac'] # [starttime, endtime, duration, startx, starty, endx, endy]
      fixations = smidata[trialnr]['events']['Efix'] # [starttime, endtime, duration, endx, endy]
    except KeyError:
      print "No eyetracking data for trial %s (image: %s)" % (trialnr + 1, imgname)
      nokey += 1
      continue
    except IndexError:
      print "No eyetracking data for trial %s (image: %s)" % (trialnr + 1, imgname)
      nokey += 1
      continue

    processed += 1
    
    # paths
    imagefile = os.path.join(imgdir, imgname)

    # rawplotfile = os.path.join(plotdir, "raw_data_%s_%d" % (ppname,trialnr))
    scatterfile = os.path.join(plotdir, "fixations_%s_%d" % (ppname,trialnr))
    scanpathfile =  os.path.join(plotdir, "scanpath_%s_%d" % (ppname,trialnr))
    heatmapfile = os.path.join(plotdir, "heatmap_%s_%d" % (ppname,trialnr))
    
    # raw data points
    # draw_raw(smidata[trialnr]['x'], smidata[trialnr]['y'], DISPSIZE, imagefile=imagefile, savefilename=rawplotfile)

    # fixations
    draw_fixations(fixations, DISPSIZE, imagefile=imagefile, durationsize=True, durationcolour=False, alpha=0.5, savefilename=scatterfile)
    
    # scanpath
    draw_scanpath(fixations, saccades, DISPSIZE, imagefile=imagefile, alpha=0.5, savefilename=scanpathfile)

    # heatmap   
    draw_heatmap(fixations, DISPSIZE, imagefile=imagefile, durationweight=True, alpha=0.75, savefilename=heatmapfile)
  print "%s images processed.  %s sections without eyetracker data." % (processed, nokey)

def usage(msg = None):
  if msg is not None:
    print msg
  print "usage: cmef-analyze-images.py <image dir> <plot dir> <smi event file> <experiment> [section.subsection ...]"
  sys.exit(1)

def main(argv):
  if len(argv) < 6:
    usage("Invalid arguments.")

  imgdir = argv[1]
  plotdir = argv[2]
  eventfile = argv[3]
  exp = load_experiment(argv[4])
  part = exp['participant']

  # try:
  lst = get_file_list(exp, argv[5:])
  process_images(lst, eventfile, part, imgdir, plotdir)

  # except Exception as exp:
  #   print str(exp)
  #   exit(1)
  # except IndexError as exp:
  #   raise exp

if '__main__' == __name__:
  main(sys.argv)
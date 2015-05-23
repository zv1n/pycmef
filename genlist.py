#!/usr/bin/env python

# cat preference.csv | grep -ho "p[0-9]\+_performance_question_[-0-9]*.png"

# cat preference.csv | cut -d, -f7 | grep -ho '[0-9]\+'
# cat performance.csv | cut -d, -f8 | grep -ho '[0-9]\+'

import sys
import json
import re

def usage(msg = None):
  if msg is not None:
    print msg
  print "usage: genlist.py <experiment> <output csv> [section.subsection ...]"
  sys.exit(1)

def qnumber(exp):
  return str(exp.get('data', {}).get('question',{}).get('number', None))

def onumber(exp):
  return str(exp.get('data', {}).get('order',-1))


def click_times(times, images):
  tlist = []
  start = times['show']
  end = times['submit']
  keys = []
  rtimes = []

  # clicknum, imagepath, time clicked, length
  for key in times:
    m = re.match(r"click([0-9]+)-image-([-0-9]+)", key)
    if m is None:
      continue
    else:
      img = int(m.group(2))
      click = int(m.group(1))
      keys.append([click, img, key])
      rtimes.append(int(times[key]))

  rtimes.append(end)
  rtimes.sort()

  durations = [j-i for i, j in zip(rtimes[:-1], rtimes[1:])]
  keys.sort(key=lambda x: x[0])

  for idx, key in enumerate(keys):
    click = key[0]
    img = key[1]
    time = int(times[key[2]])

    tlist.append([ str(click), str(images[img]), str(durations[idx]), str(time - start) ])
  
  tlist.sort(key=lambda x: x[0])

  return tlist


def get_click_data(exp, components):
  top = exp
  for comp in components:
    top = top.get(comp, None)
    if top is None:
      return []

  # onum, qnum, clicknum, imagepath, time clicked, length
  dlist = []
  for item in top:
    onum = onumber(item)
    qnum = qnumber(item)

    times = item.get('times', {})
    images = item.get('data', {}).get('image_set', [])
    cdata = click_times(times, images)

    for d in cdata:
      lst = [onum, qnum]
      lst.extend(d)
      dlist.append(lst)

  return dlist


def get_image_clicks(fle, components):
  with open(fle, 'rb') as jsonfile:
    exp = json.load(jsonfile)
    data = [['order', 'question', 'click', 'image', 'view duration', 'clicked at']]

    for comp in components:
      dlist = get_click_data(exp, comp.split('.'))
      data.extend(dlist)

  return data


def main(argv):
  if len(argv) < 4:
    usage("Invalid arguments.")

  lst = get_image_clicks(argv[1], argv[3:])

  with open(argv[2], "w") as handle:
    for f in lst:
      handle.write(", ".join(f))
      handle.write("\n")

  print "%s click events written to file." % (len(lst) - 1)

if __name__ == "__main__":
  main(sys.argv)
#!/usr/bin/env python
import os
import sys

sys.argv.pop(0)
output = sys.argv.pop(0)

with open(output, 'w') as f:
  for file in sys.argv:
    with open(file, 'r') as r:
      f.write(r.read())
    f.write("\n")

print "%s files appeneded." % len(sys.argv)

#!/usr/bin/env python

from subprocess import call
import os, time, glob, re

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CoffeeWatcher(FileSystemEventHandler):
  def on_any_event(self, event):
    m = re.search("coffee$", event.src_path)
    if m is None:
      print "Skipping: %s" % event.src_path
      return

    print "File event: %s" % event.src_path
    call(['coffee', '-c', event.src_path])

def main():
  os.chdir('cmef')
  print 'Starting watcher...'

  watcher = CoffeeWatcher()
  observer = Observer()
  observer.schedule(watcher, '.', recursive=True)
  observer.start()

  try:
      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()

  observer.join()

if __name__ == "__main__":
  main()

import random

class Iterator:
  def set_range(self, low, high):
    self.range = range(low, high)
    self.length = len(self.range)

  def count(self):
    return self.length - len(self.range) - 1

  def done(self):
    return (len(self.range) == 0)

class SequentialIterator(Iterator):
  def next(self):
    return self.range.pop(0)

  def type(self):
    return 'sequential'

class RandomIterator(Iterator):
  def next(self):
    idx = random.randint(0, len(self.range)-1)
    return self.range.pop(idx)

  def type(self):
    return 'random:dependent'
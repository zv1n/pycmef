
import random

class Iterator:
  def set_range(self, low, high):
    self.range = range(low, high)

  def done(self):
    return (len(self.range) == 0)

class SequentialIterator(Iterator):
  def next(self):
    return self.range.pop(0)

class RandomIterator(Iterator):
  def next(self):
    idx = random.randint(0, len(self.range)-1)
    return self.range.pop(idx)

  
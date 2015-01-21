
import random, re

class Iterator(object):
  def set_range(self, low, high):
    self.range = range(low, high)
    self.length = len(self.range)

  def count(self):
    return self.length - len(self.range) - 1

  def done(self):
    return (len(self.range) == 0)


class SequentialIterator(Iterator):
  def __init__(self, order):
    pass

  def next(self):
    try:
      return self.range.pop(0)
    except IndexError:
      return None

  @staticmethod
  def type():
    return 'sequential'

  @staticmethod
  def is_type(type):
    return type == SequentialIterator.type()


class RandomIterator(Iterator):
  def __init__(self, order):
    pass

  def next(self):
    try:
      idx = random.randint(0, len(self.range)-1)
      return self.range.pop(idx)
    except IndexError:
      return None

  @staticmethod
  def type():
    return 'random:dependent'

  @staticmethod
  def is_type(type):
    return type == RandomIterator.type()


class RandomGroup(Iterator):
  groups = {}

  def __init__(self, order):
    self.group = RandomGroup.get_group(order)
    self.list = []

  def count(self):
    return self.length - len(self.list) - 1

  def set_range(self, low, high):
    list = RandomGroup.groups.get(self.group, None)

    if list is None:
      self.create_group_list(low, high)
    else:
      self.list = list[:]
      self.length = len(self.list)
      self.range = []

  def create_group_list(self, low, high):
    super(RandomGroup, self).set_range(low, high)

    for i in range(0, self.length):
      idx = random.randint(0, len(self.range)-1)
      self.list.append(self.range.pop(idx))

    RandomGroup.groups[self.group] = self.list[:]

  @staticmethod
  def get_group(order):
    m = re.match(r'^\s*random:dependent:group\(([a-zA-Z0-9]+)\)\s*$', order)

    if m is None:
      return None
    return m.group(0)

  def next(self):
    try:
      return self.list.pop(0)
    except IndexError:
      return None

  def done(self):
    return len(self.list) == 0

  @staticmethod
  def is_type(type):
    if RandomGroup.get_group(type) is None:
      return False
    return True

  @staticmethod
  def type():
    return 'random:dependent:group'

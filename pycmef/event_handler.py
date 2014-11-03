
import json

def returns_dictionary(func):
  def inner(*args, **kwargs):    
    result = func(*args, **kwargs)

    if not isinstance(result, dict):
      raise Exception('Method should return a Dictionary object.')

    return json.dumps(result)
  return inner

def returns_list(func, *args, **kwargs):
  def inner(*args, **kwargs):    
    result = func(*args, **kwargs)

    if not isinstance(result, list):
      raise Exception('Method should return a List object.')

    return json.dumps(result)
  return inner

def returns_string(func, *args, **kwargs):
  def inner(*args, **kwargs):    
    result = func(*args, **kwargs)

    if not isinstance(result, str):
      raise Exception('Method should return a String object.')

    return result
  return inner

class EventHandler:
  def __init__(self):
    pass

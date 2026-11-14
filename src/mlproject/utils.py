from copy import deepcopy
from itertools import product

def deep_merge(base: dict, override: dict) -> dict:
  result = deepcopy(base)
  for key, value in override.items():
    if (
      key in result
      and isinstance(result[key], dict)
      and isinstance(value, dict)
    ):
      result[key] = deep_merge(result[key], value)
    else:
      result[key] = deepcopy(value)
  return result

def generate_dict_combinations(data: dict):
  if not data:
    yield {}
    return
  keys = list(data.keys())
  for values in product(*data.values()):
    yield dict(zip(keys, values))


def generate_list_combinations(data: list):
  if not data:
    yield ()
    return
  if all(isinstance(item, list) for item in data):
    yield from product(*data)
  else:
    yield from ((item,) for item in data)

def generate_combinations(data):
  if isinstance(data, dict):
    if not data:
      yield {}
      return
    keys = list(data.keys())
    options = [
      list(generate_combinations(value))
      for value in data.values()
    ]
    for values in product(*options):
      yield dict(zip(keys, values))
  elif isinstance(data, list):
    if not data:
      yield None
    else:
      yield from data
  else:
    yield data

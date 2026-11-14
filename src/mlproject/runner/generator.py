from itertools import product
import src.mlproject.utils as utils

def generate_cleaning_config(config: dict):
  if not config.get("enable", False):
    return [{"enable": False}]

  missing_values = config.get("missing_values", {})
  duplicated = config.get("duplicated", {})

  missing_configs = list(
    utils.generate_combinations(missing_values)
  ) if missing_values else [{}]

  if duplicated.get("enable", False):
    duplicated_configs = [
      {
        "enable": True,
        "keep": keep
      }
      for keep in utils.generate_combinations(
        duplicated.get("keep", ["first"])
      )
    ]
  else:
    duplicated_configs = [{"enable": False}]

  return [
    {
      "enable": True,
      "missing_values": missing,
      "duplicated": duplicate
    }
    for missing, duplicate in product(
      missing_configs,
      duplicated_configs
    )
  ]

def generate_splitting_config(config: dict):
  return [
    item
    for item in utils.generate_combinations(config)
    if not (
      item["holdout"] is None
      and item["cv"] is None
    )
  ]

def generate_transformation_config(config: dict):
  if not config.get("enable", False):
    return [{"enable": False}]

  numeric_configs = utils.generate_combinations(
    config.get("numeric", {})
  )

  categorical_configs = utils.generate_combinations(
    config.get("categorical", {})
  )

  return [
    {
      "enable": True,
      "numeric": numeric,
      "categorical": categorical
    }
    for numeric, categorical in product(
      numeric_configs,
      categorical_configs
    )
  ]

def generate_preprocessing_config(config: list):
  cleaning_config, splitting_config, transformation_config = config

  cleaning_configs = generate_cleaning_config(
    cleaning_config
  )

  splitting_configs = list(
    utils.generate_combinations(splitting_config)
  )

  splitting_configs = [
    item
    for item in splitting_configs
    if not (
      item["holdout"] is None
      and item["cv"] is None
    )
  ]

  transformation_configs = generate_transformation_config(
    transformation_config
  )

  return [
    {
      "clean": clean,
      "split": split,
      "transform": transform
    }
    for clean, split, transform in product(
      cleaning_configs,
      splitting_configs,
      transformation_configs
    )
  ]

from mlproject.config import load_experiment_config, get_experiment_config, get_default_config
from mlproject.data import loader
from mlproject.runner.generator import generate_preprocessing_config

def runner(experiment_name: str) -> None:
  experiment_config = load_experiment_config()
  print(experiment_config.get(experiment_name))

  (experiment_dataset, experiment_preprocessing,
   experiment_model, experiment_runs) \
    = get_experiment_config(experiment_name, experiment_config)
  dataset_key, _, _, _ = experiment_dataset
  dataset_bundle = loader.load_dataset(dataset_key)

  preprocessing_default_config, models_default_config = get_default_config()

  preprocessing_configs \
    = list(
    generate_preprocessing_config(
      experiment_preprocessing,
      list(preprocessing_default_config)
    )
  )
  print(preprocessing_configs)

"""
  This section is for runs config overrides
  It overrides experiment config
  For each overrides it runs this experiments
  
  In runs, we merge config (clean, split, transform and model) 
  with default config
  
  Pseudo code:
  
  Clone experiment config
  Overrides config
  for each runs overrides 
    merge config + default config
    
    run preprocessing     |
      run modeling        | this section run independence
        run evaluation    | i tab this to make easier for imagine
        save evaluation
    
        get result evaluation
        combination config + result
        save result + combination config
    end this run
  summary runs  
"""
  # Merge config

if __name__ == "__main__":
  runner(experiment_name="A_full_dataset")
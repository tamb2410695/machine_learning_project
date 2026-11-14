from mlproject.config import load_experiment_config, get_experiment_config
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
  # print(dataset_bundle.frame)
  preprocessing_configs = list(generate_preprocessing_config(experiment_preprocessing))
  print(preprocessing_configs)
  # print(experiment_preprocessing)
  # print(experiment_model)
  # print(experiment_runs)
  # eda_section(dataset_bundle.frame, dataset_bundle.columns)

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
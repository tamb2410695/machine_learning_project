2 type of config:
  Experiment config: save run config
  Default config: default config for python file 
    - all of this should save in dataclass, 
      and use product fn to make combination for each experiment

Create registry config at python to link dataclass and runner  

Sample default config:
split:
  holdout:
    parameter

  kfold:
    parameter

transform:
  minmax:
    parameter
  standard:
    parameter

model:
  decision_tree:
    name: 
    id
    parameter_grid

Sample baseline config (experiments):
dataset_name:
  experiment:
    task: task_name
    target:
    features:
      numeric
      categorical
  
    preprocessing:
      clean
      split
        stragety: []
        
      transform
  
    model:
      name:
      metric:
      refit:
    
    evaluation:
      metrics





Quy uoc
Không override model
yaml

model:
  random_forest_regressor:

Dùng nguyên cấu hình gốc.

Override một phần
yaml

model:
  random_forest_regressor:
    enable: false

Chỉ đổi enable; các trường còn lại giữ nguyên.

Override một phần parameter grid
yaml

model:
  random_forest_regressor:
    parameter_grid:
      n_estimators: [300, 500]

Chỉ thay grid của n_estimators; các grid khác giữ nguyên.



Quy tắc chuẩn đề xuất

Giá trị override
	

Hành vi

Key không tồn tại
	

Giữ giá trị gốc

null ở cấp model
	

Dùng toàn bộ cấu hình gốc của model

null ở một trường con
	

Ghi đè thành None, trừ khi trường đó có quy tắc riêng

Dictionary
	

Merge đệ quy

List
	

Thay thế toàn bộ list gốc

List rỗng []
	

Ghi đè thành list rỗng

Giá trị scalar (str, int, bool,...)
	

Ghi đè giá trị gốc




A_full_dataset:
  dataset_key: kerala_house_price
  task: regression
  target: price

  features:
    numeric: []
    categorical: []

  preprocessing:
    clean:
      enable: true
      missing_values:
        enabled: true
        markers: ["", "nan", "null", "none", "na", "n/a"]
        strategy:
          numeric: median
          categorical: most_frequent
        drop_rows_if_target_missing: true

      duplicated:
        enabled: true
        mode: search
        strategy_candidates: [keep, drop_first, drop_last]
        keep: first
        subset: null

    split:
      holdout: [null, 0.2, 0.3, 0.4]
      cv: [null, 5, 6, 7, 8]

    transform:
      enable: true

  model:
    decision_tree_regressor:
      parameter_grid: []

    random_forest_regressor: null
    k_nearest_neighbors_regressor: null
    linear_regression: null

  runs:
    - name: baseline
      overrides: {}

    - name: clean_disabled
      overrides:
        preprocessing:
          clean:
            enable: false

    - name: transform_disabled
      overrides:
        preprocessing:
          transform:
            enable: false

    - name: model_search
      overrides:
        model:
          random_forest_regressor:
            parameter_grid:
              n_estimators: [100, 200, 300]
              max_depth: [null, 10, 20]

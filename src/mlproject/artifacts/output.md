outputs/
└── kerala_house_price/
    └── regression/
        ├── experiments/
        │   ├── keep_duplicates/
        │   │   ├── config.yaml
        │   │   ├── model_results.csv
        │   │   ├── best_model.json
        │   │   └── cv_results/
        │   │       ├── dt.csv
        │   │       ├── rf.csv
        │   │       └── knn.csv
        │   │
        │   └── drop_duplicates/
        │       ├── config.yaml
        │       ├── model_results.csv
        │       ├── best_model.json
        │       └── cv_results/
        │           ├── dt.csv
        │           ├── rf.csv
        │           └── knn.csv
        │
        └── comparisons/
            ├── within_experiment/
            │   ├── keep_duplicates.csv
            │   └── drop_duplicates.csv
            ├── across_experiments/
            │   ├── decision_tree.csv
            │   ├── random_forest.csv
            │   └── knn.csv
            └── overall/
                ├── experiment_comparison.csv
                └── plots/
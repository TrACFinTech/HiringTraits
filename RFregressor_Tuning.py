import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import itertools

with open('/Users/tirthoroy/Desktop/FinTech/InputTraitScores(outOf5).json', 'r') as f:
    input_data = json.load(f)

with open('GroundTruth(outOf7).json', 'r') as f:
    ground_truth_data = json.load(f)

input_df = pd.DataFrame(input_data).T

gt_df = pd.DataFrame({k: v['RecommendHiring'] for d in ground_truth_data for k, v in d.items()}, index=[0]).T
gt_df.columns = ['RecommendHiring']

df = input_df.merge(gt_df, left_index=True, right_index=True, how='inner')

X = df.drop('RecommendHiring', axis=1)
y = df['RecommendHiring']

n_estimators_options = [50, 100, 150, 200, 250, 300]
max_depth_options = [None, 5, 10, 15, 20, 25, 30]
min_samples_split_options = [2, 5, 10, 15, 20]
min_samples_leaf_options = [1, 2, 4, 6, 8]
max_features_options = ['sqrt', 'log2', None]  # Removed 'auto'

param_combinations = list(itertools.product(n_estimators_options, max_depth_options, min_samples_split_options, min_samples_leaf_options, max_features_options))

if len(param_combinations) < 10000:
    extra_options = list(itertools.product(
        [400, 500],
        [35, 40],
        [25, 30],
        [10, 12],
        [None]
    ))
    param_combinations.extend(extra_options[:10000 - len(param_combinations)])

results_list = []

for i, (n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features) in enumerate(param_combinations):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=42,
        max_features=max_features,
        bootstrap=True
    )
    
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    results_list.append({
        'Combination': i,
        'n_estimators': n_estimators,
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
        'max_features': max_features,
        'Mean Squared Error': mse,
        'R^2 Score': r2
    })

results_df = pd.DataFrame(results_list)

excel_filename = 'model_tuning_results.xlsx'
with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
    results_df.to_excel(writer, sheet_name='Results', index=False)

print(f"Results saved to {excel_filename}")

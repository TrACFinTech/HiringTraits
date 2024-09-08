import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load the JSON data
with open('InputTraitScores(outOf5).json', 'r') as f:
    input_data = json.load(f)

with open('GroundTruth(outOf7).json', 'r') as f:
    ground_truth_data = json.load(f)

# Convert input data to DataFrame
input_df = pd.DataFrame(input_data).T  # Transpose so each row represents a person

# Convert ground truth data to DataFrame
gt_df = pd.DataFrame({k: v['RecommendHiring'] for d in ground_truth_data for k, v in d.items()}, index=[0]).T
gt_df.columns = ['RecommendHiring']

# Merge input traits with ground truth to form the dataset
df = input_df.merge(gt_df, left_index=True, right_index=True, how='inner')

# Split the data into features (X) and target (y)
X = df.drop('RecommendHiring', axis=1)
y = df['RecommendHiring']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Regressor
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    max_features='sqrt',
    bootstrap=True
)

# Fit the model
rf_model.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Print predictions for test set
print("Predictions:", y_pred)

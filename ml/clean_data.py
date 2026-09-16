import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("../data/mplads_historical_clean.csv")

print("Original shape:", df.shape)

# Features for our first ML model
features = [
    "funds_available",
    "sanctioned_funds",
    "actual_expenditure",
    "works_sanctioned",
    "works_completed",
    "pending_works",
    "pct_completed",
    "pct_utilisation",
    "expenditure_to_sanctioned_pct",
    "pending_share_pct",
    "completion_gap_pct",
    "avg_sanction_per_work_lakh"
]

# Keep only required columns + identifiers
clean_df = df[
    ["constituency", "year"] + features
].copy()

# Replace infinite values with NaN
clean_df = clean_df.replace([np.inf, -np.inf], np.nan)

print("\nMissing values BEFORE cleaning:")
print(clean_df[features].isnull().sum())

# Fill missing values using median of each feature
# Median is safer than mean when data contains extreme values.
for column in features:
    clean_df[column] = clean_df[column].fillna(
        clean_df[column].median()
    )

print("\nMissing values AFTER cleaning:")
print(clean_df[features].isnull().sum())

# Save cleaned dataset
output_file = "../data/ml_ready_data.csv"

clean_df.to_csv(output_file, index=False)

print("\nCleaned dataset saved to:")
print(output_file)

print("\nFinal shape:", clean_df.shape)
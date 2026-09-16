import pandas as pd

# Dataset ka path
file_path = "../data/mplads_historical_clean.csv"

# Dataset load karo
df = pd.read_csv(file_path)

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())
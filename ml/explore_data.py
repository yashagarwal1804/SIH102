import pandas as pd

df = pd.read_csv("../data/mplads_historical_clean.csv")

print("\n===== STATISTICS =====")
print(df.describe())

print("\n===== UNIQUE CONSTITUENCIES =====")
print(df["constituency"].unique())

print("\n===== YEARS =====")
print(sorted(df["year"].unique()))

print("\n===== SAMPLE DATA =====")
print(
    df[
        [
            "constituency",
            "year",
            "funds_available",
            "sanctioned_funds",
            "actual_expenditure",
            "works_sanctioned",
            "works_completed",
            "pending_works",
            "pct_completed",
            "pct_utilisation"
        ]
    ].head(20)
)
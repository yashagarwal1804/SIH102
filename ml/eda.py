import pandas as pd
import matplotlib.pyplot as plt

# Load ML-ready dataset
df = pd.read_csv("../data/ml_ready_data.csv")

print("Dataset shape:", df.shape)

# ------------------------------------------------
# 1. Basic statistics
# ------------------------------------------------

print("\n===== BASIC STATISTICS =====")
print(df.describe())


# ------------------------------------------------
# 2. Average values by year
# ------------------------------------------------

year_data = df.groupby("year")[
    [
        "funds_available",
        "actual_expenditure",
        "works_sanctioned",
        "works_completed",
        "pending_works",
        "pct_completed",
        "pct_utilisation"
    ]
].mean()

print("\n===== YEARLY AVERAGES =====")
print(year_data)


# ------------------------------------------------
# 3. Average utilization by constituency
# ------------------------------------------------

constituency_utilisation = df.groupby(
    "constituency"
)["pct_utilisation"].mean().sort_values()

print("\n===== AVERAGE UTILISATION =====")
print(constituency_utilisation)


# ------------------------------------------------
# 4. Average pending works
# ------------------------------------------------

pending = df.groupby(
    "constituency"
)["pending_works"].mean().sort_values(ascending=False)

print("\n===== AVERAGE PENDING WORKS =====")
print(pending)


# ------------------------------------------------
# 5. Plot utilization
# ------------------------------------------------

plt.figure(figsize=(12, 6))

constituency_utilisation.plot(kind="bar")

plt.title("Average MPLADS Fund Utilisation")
plt.xlabel("Constituency")
plt.ylabel("Utilisation (%)")

plt.xticks(rotation=75)
plt.tight_layout()

plt.savefig("../data/utilisation_chart.png")

plt.show()


# ------------------------------------------------
# 6. Plot pending works
# ------------------------------------------------

plt.figure(figsize=(12, 6))

pending.plot(kind="bar")

plt.title("Average Pending Works")
plt.xlabel("Constituency")
plt.ylabel("Pending Works")

plt.xticks(rotation=75)
plt.tight_layout()

plt.savefig("../data/pending_works_chart.png")

plt.show()
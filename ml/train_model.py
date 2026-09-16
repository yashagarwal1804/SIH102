import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("../data/ml_ready_data.csv")

print("Dataset shape:", df.shape)


# ==========================================
# 2. SELECT ML FEATURES
# ==========================================

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

X = df[features].copy()


# ==========================================
# 3. SCALE FEATURES
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ==========================================
# 4. TRAIN ISOLATION FOREST
# ==========================================

model = IsolationForest(
    n_estimators=200,
    contamination=0.10,
    random_state=42
)

model.fit(X_scaled)


# ==========================================
# 5. GENERATE ANOMALY SCORES
# ==========================================

df["anomaly_prediction"] = model.predict(X_scaled)

df["anomaly_score"] = model.decision_function(X_scaled)


# ==========================================
# 6. CONVERT TO RISK SCORE
# ==========================================

# Lower Isolation Forest score = more anomalous

min_score = df["anomaly_score"].min()
max_score = df["anomaly_score"].max()

df["risk_score"] = (
    (max_score - df["anomaly_score"])
    / (max_score - min_score)
) * 100


# ==========================================
# 7. RISK CATEGORY
# ==========================================

def risk_category(score):

    if score >= 75:
        return "HIGH"

    elif score >= 50:
        return "MEDIUM"

    else:
        return "LOW"


df["risk_category"] = df["risk_score"].apply(risk_category)


# ==========================================
# 8. SAVE RESULTS
# ==========================================

output_file = "../data/anomaly_results.csv"

df.to_csv(output_file, index=False)

print("\n===== TOP ANOMALOUS RECORDS =====")

top_records = df.sort_values(
    "risk_score",
    ascending=False
)

print(
    top_records[
        [
            "constituency",
            "year",
            "risk_score",
            "risk_category",
            "pending_works",
            "pct_utilisation",
            "pct_completed"
        ]
    ].head(15)
)


# ==========================================
# 9. SAVE MODEL + SCALER
# ==========================================

joblib.dump(model, "../data/isolation_forest.pkl")
joblib.dump(scaler, "../data/scaler.pkl")

print("\nModel saved:")
print("../data/isolation_forest.pkl")

print("\nResults saved:")
print(output_file)
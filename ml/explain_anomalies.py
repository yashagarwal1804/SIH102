import pandas as pd

# ==========================================
# 1. LOAD ANOMALY RESULTS
# ==========================================

df = pd.read_csv("../data/anomaly_results.csv")


# ==========================================
# 2. GENERATE EXPLANATION
# ==========================================

def generate_reasons(row):

    reasons = []

    # High pending works
    if row["pending_works"] > 700:
        reasons.append(
            "Very high number of pending works"
        )

    # Low completion
    if row["pct_completed"] < 40:
        reasons.append(
            "Very low percentage of completed works"
        )

    # Low utilisation
    if row["pct_utilisation"] < 60:
        reasons.append(
            "Low fund utilisation"
        )

    # High utilisation but low completion
    if (
        row["pct_utilisation"] > 85
        and row["pct_completed"] < 50
    ):
        reasons.append(
            "High fund utilisation but low work completion"
        )

    # Large pending share
    if row["pending_share_pct"] > 50:
        reasons.append(
            "Large share of works remain pending"
        )

    # Large completion gap
    if row["completion_gap_pct"] > 40:
        reasons.append(
            "Large gap between sanctioned and completed works"
        )

    # Unusually large sanction per work
    if row["avg_sanction_per_work_lakh"] > 20:
        reasons.append(
            "Unusually high average sanction per work"
        )

    # If no rule triggered
    if len(reasons) == 0:
        reasons.append(
            "Unusual combination of multiple financial and work indicators"
        )

    return reasons


# ==========================================
# 3. APPLY EXPLANATIONS
# ==========================================

df["risk_reasons"] = df.apply(
    generate_reasons,
    axis=1
)


# ==========================================
# 4. SAVE
# ==========================================

output_file = "../data/explained_anomalies.csv"

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 5. SHOW HIGH-RISK CASES
# ==========================================

high_risk = df[
    df["risk_category"] == "HIGH"
].sort_values(
    "risk_score",
    ascending=False
)


print("\n===== AI EXPLANATIONS =====\n")

for _, row in high_risk.head(10).iterrows():

    print(
        f"{row['constituency']} - {int(row['year'])}"
    )

    print(
        f"Risk Score: {row['risk_score']:.2f}"
    )

    print("Reasons:")

    for reason in row["risk_reasons"]:
        print(f"  - {reason}")

    print("-" * 50)


print("\nSaved:")
print(output_file)
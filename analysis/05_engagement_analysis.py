import pandas as pd
from pathlib import Path

# ============================================================
# 1. Define project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "cookie_cats.csv"

# ============================================================
# 2. Load dataset
# ============================================================

df = pd.read_csv(DATA_PATH)

# ============================================================
# 3. Overall engagement statistics
# ============================================================

print("\n" + "=" * 65)
print("COOKIE CATS — PLAYER ENGAGEMENT ANALYSIS")
print("=" * 65)

print("\n1. Overall Game Rounds Distribution:")

overall_stats = df["sum_gamerounds"].describe(
    percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
)

print(overall_stats)

# ============================================================
# 4. Engagement by experimental group
# ============================================================

print("\n2. Engagement by Experimental Group:")

engagement_summary = (
    df.groupby("version")["sum_gamerounds"]
    .agg(
        players="count",
        mean="mean",
        median="median",
        std="std",
        min="min",
        max="max"
    )
)

print(engagement_summary.round(2))

# ============================================================
# 5. Distribution percentiles by group
# ============================================================

print("\n3. Game Rounds Percentiles by Group:")

percentiles = (
    df.groupby("version")["sum_gamerounds"]
    .quantile([0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
    .unstack()
)

percentiles.columns = [
    "P25", "P50", "P75", "P90", "P95", "P99"
]

print(percentiles.round(2))

# ============================================================
# 6. Zero-round players
# ============================================================

print("\n4. Players with Zero Game Rounds:")

zero_rounds = (
    df.assign(
        zero_rounds=df["sum_gamerounds"] == 0
    )
    .groupby("version")
    .agg(
        total_players=("userid", "count"),
        zero_round_players=("zero_rounds", "sum"),
        zero_round_rate=("zero_rounds", "mean")
    )
)

zero_rounds["zero_round_rate"] *= 100

print(zero_rounds.round(2))

# ============================================================
# 7. Identify potentially extreme observations
# ============================================================

print("\n5. Potential Outlier Assessment (IQR Method):")

q1 = df["sum_gamerounds"].quantile(0.25)
q3 = df["sum_gamerounds"].quantile(0.75)

iqr = q3 - q1

upper_bound = q3 + 1.5 * iqr

potential_outliers = (
    df["sum_gamerounds"] > upper_bound
).sum()

print(f"Q1: {q1:.2f}")
print(f"Q3: {q3:.2f}")
print(f"IQR: {iqr:.2f}")
print(f"Upper outlier threshold: {upper_bound:.2f}")
print(f"Observations above threshold: {potential_outliers:,}")

# ============================================================
# 8. Conclusion
# ============================================================

print("\n" + "=" * 65)
print("ENGAGEMENT EXPLORATION COMPLETED")
print("=" * 65)

import pandas as pd
from pathlib import Path

# ============================================================
# 1. Define project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "cookie_cats.csv"

# ============================================================
# 2. Load the dataset
# ============================================================

df = pd.read_csv(DATA_PATH)

# ============================================================
# 3. Overall player retention
# ============================================================

print("\n" + "=" * 60)
print("COOKIE CATS — PLAYER RETENTION ANALYSIS")
print("=" * 60)

total_players = len(df)

day1_retained = df["retention_1"].sum()
day7_retained = df["retention_7"].sum()

day1_rate = day1_retained / total_players * 100
day7_rate = day7_retained / total_players * 100

print("\n1. Overall Player Retention:")
print(f"Total players: {total_players:,}")
print(f"Day 1 retained players: {day1_retained:,}")
print(f"Day 1 retention rate: {day1_rate:.2f}%")
print(f"Day 7 retained players: {day7_retained:,}")
print(f"Day 7 retention rate: {day7_rate:.2f}%")

# ============================================================
# 4. Retention by experiment group
# ============================================================

retention_summary = (
    df.groupby("version")
    .agg(
        total_players=("userid", "count"),
        day1_retained=("retention_1", "sum"),
        day7_retained=("retention_7", "sum"),
        day1_retention=("retention_1", "mean"),
        day7_retention=("retention_7", "mean")
    )
    .reset_index()
)

# Convert proportions to percentages
retention_summary["day1_retention"] *= 100
retention_summary["day7_retention"] *= 100

print("\n2. Retention by Experimental Group:")
print(retention_summary.to_string(index=False, float_format="%.2f"))

# ============================================================
# 5. Calculate differences between groups
# ============================================================

gate30 = retention_summary.set_index("version").loc["gate_30"]
gate40 = retention_summary.set_index("version").loc["gate_40"]

day1_difference = (
    gate40["day1_retention"] - gate30["day1_retention"]
)

day7_difference = (
    gate40["day7_retention"] - gate30["day7_retention"]
)

print("\n3. Treatment Effect — Descriptive Comparison:")
print(f"Day 1 retention difference: {day1_difference:+.3f} percentage points")
print(f"Day 7 retention difference: {day7_difference:+.3f} percentage points")

# ============================================================
# 6. Calculate relative changes
# ============================================================

day1_relative = (
    day1_difference / gate30["day1_retention"] * 100
)

day7_relative = (
    day7_difference / gate30["day7_retention"] * 100
)

print("\n4. Relative Changes Compared with Gate 30:")
print(f"Day 1 relative change: {day1_relative:+.2f}%")
print(f"Day 7 relative change: {day7_relative:+.2f}%")

# ============================================================
# 7. Summary
# ============================================================

print("\n" + "=" * 60)
print("RETENTION EXPLORATION COMPLETED")
print("=" * 60)
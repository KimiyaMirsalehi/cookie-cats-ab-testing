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
# 3. Identify the 10 most active players
# ============================================================

print("\n" + "=" * 65)
print("COOKIE CATS — EXTREME PLAYER ACTIVITY INVESTIGATION")
print("=" * 65)

top_players = df.nlargest(10, "sum_gamerounds")

print("\n1. Top 10 Players by Game Rounds:")
print(top_players.to_string(index=False))

# ============================================================
# 4. Calculate original engagement statistics
# ============================================================

original_stats = (
    df.groupby("version")["sum_gamerounds"]
    .agg(["count", "mean", "median", "std"])
)

print("\n2. Original Engagement Statistics:")
print(original_stats.round(2))

# ============================================================
# 5. Sensitivity analysis: exclude the single largest value
# ============================================================

max_rounds = df["sum_gamerounds"].max()

max_player = df.loc[
    df["sum_gamerounds"].idxmax()
]

# Create a temporary analytical copy
df_sensitivity = df.drop(index=df["sum_gamerounds"].idxmax())

sensitivity_stats = (
    df_sensitivity.groupby("version")["sum_gamerounds"]
    .agg(["count", "mean", "median", "std"])
)

print("\n3. Engagement Statistics Excluding the Largest Observation:")
print(sensitivity_stats.round(2))

# ============================================================
# 6. Compare group means
# ============================================================

original_difference = (
    original_stats.loc["gate_40", "mean"]
    - original_stats.loc["gate_30", "mean"]
)

adjusted_difference = (
    sensitivity_stats.loc["gate_40", "mean"]
    - sensitivity_stats.loc["gate_30", "mean"]
)

print("\n4. Sensitivity Analysis — Difference in Mean Rounds:")

print(f"Original difference (Gate 40 - Gate 30): {original_difference:+.3f}")

print(f"Excluding largest observation: {adjusted_difference:+.3f}")

# ============================================================
# 7. Display extreme observation details
# ============================================================

print("\n5. Largest Observation:")

print(f"Player ID: {max_player['userid']}")
print(f"Experiment group: {max_player['version']}")
print(f"Game rounds: {max_rounds:,}")
print(f"Day 1 retention: {max_player['retention_1']}")
print(f"Day 7 retention: {max_player['retention_7']}")

print("\n" + "=" * 65)
print("OUTLIER INVESTIGATION COMPLETED")
print("=" * 65)

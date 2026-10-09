import numpy as np
import pandas as pd

from pathlib import Path

# ============================================================
# 1. Define project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "cookie_cats.csv"

# ============================================================
# 2. Define experiment settings
# ============================================================

CONTROL = "gate_30"
TREATMENT = "gate_40"

METRIC = "sum_gamerounds"

N_PERMUTATIONS = 5000
RANDOM_SEED = 42
ALPHA = 0.05

# ============================================================
# 3. Load and validate data
# ============================================================

df = pd.read_csv(DATA_PATH)

assert df[METRIC].notna().all(), "Missing game-round values detected."
assert df["version"].isin([CONTROL, TREATMENT]).all(), (
    "Unexpected experimental group detected."
)

# ============================================================
# 4. Calculate observed difference in means
# ============================================================

control_values = df.loc[
    df["version"] == CONTROL, METRIC
].to_numpy(dtype=float)

treatment_values = df.loc[
    df["version"] == TREATMENT, METRIC
].to_numpy(dtype=float)

observed_difference = (
    treatment_values.mean() - control_values.mean()
)

print("\n" + "=" * 65)
print("COOKIE CATS — ENGAGEMENT PERMUTATION TEST")
print("=" * 65)

print("\n1. Original Engagement Statistics:")

print(f"Control players: {len(control_values):,}")
print(f"Treatment players: {len(treatment_values):,}")

print(f"Control mean rounds: {control_values.mean():.4f}")
print(f"Treatment mean rounds: {treatment_values.mean():.4f}")

print(
    f"Observed difference (Treatment - Control): "
    f"{observed_difference:+.4f}"
)

# ============================================================
# 5. Perform permutation test
# ============================================================

rng = np.random.default_rng(RANDOM_SEED)

all_values = np.concatenate([
    treatment_values,
    control_values
])

n_treatment = len(treatment_values)
n_total = len(all_values)

# Keep the original group sizes unchanged during permutations
permutation_differences = np.empty(N_PERMUTATIONS)

print("\n2. Running Permutation Test...")

for i in range(N_PERMUTATIONS):

    shuffled = rng.permutation(all_values)

    treatment_mean = shuffled[:n_treatment].mean()
    control_mean = shuffled[n_treatment:].mean()

    permutation_differences[i] = (
        treatment_mean - control_mean
    )

# ============================================================
# 6. Calculate two-sided permutation p-value
# ============================================================

extreme_count = np.sum(
    np.abs(permutation_differences)
    >= abs(observed_difference)
)

p_value = (extreme_count + 1) / (N_PERMUTATIONS + 1)

print("\n3. Permutation Test Results:")

print(f"Number of permutations: {N_PERMUTATIONS:,}")
print(f"Random seed: {RANDOM_SEED}")
print(f"Observed difference: {observed_difference:+.4f}")
print(f"Two-sided permutation p-value: {p_value:.6f}")

# ============================================================
# 7. Statistical interpretation
# ============================================================

print("\n4. Statistical Interpretation:")

if p_value < ALPHA:
    print(
        "Result: Statistically significant difference "
        "in mean game rounds at the 5% level."
    )
else:
    print(
        "Result: No statistically significant difference "
        "in mean game rounds at the 5% level."
    )

# ============================================================
# 8. Additional descriptive statistics
# ============================================================

print("\n5. Median Engagement:")

print(f"Control median: {np.median(control_values):.2f}")
print(f"Treatment median: {np.median(treatment_values):.2f}")

print(
    "Note: This test evaluates the difference in means, "
    "not the difference in medians."
)

print("\n6. Methodological Notes:")

print(
    "- All observations are retained.\n"
    "- Group sizes remain fixed during permutation.\n"
    "- The test assumes exchangeability of group labels "
    "under the null hypothesis.\n"
    "- Extreme observations can influence mean differences.\n"
    "- Engagement is a secondary, exploratory outcome."
)

print("\n" + "=" * 65)
print("ENGAGEMENT PERMUTATION TEST COMPLETED")
print("=" * 65)
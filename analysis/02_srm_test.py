import pandas as pd
from pathlib import Path
from scipy.stats import chisquare

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
# 3. Define expected experiment allocation
# ============================================================

# Assumption: players should be allocated equally (50/50)
EXPECTED_ALLOCATION = {
    "gate_30": 0.50,
    "gate_40": 0.50
}

# Conservative significance threshold for SRM detection
ALPHA = 0.001

# ============================================================
# 4. Calculate observed and expected sample sizes
# ============================================================

observed_counts = (
    df["version"]
    .value_counts()
    .reindex(EXPECTED_ALLOCATION.keys(), fill_value=0)
)

total_players = observed_counts.sum()

expected_counts = pd.Series({
    group: total_players * proportion
    for group, proportion in EXPECTED_ALLOCATION.items()
})

# ============================================================
# 5. Perform Chi-Square Goodness-of-Fit Test
# ============================================================

chi2_statistic, p_value = chisquare(
    f_obs=observed_counts,
    f_exp=expected_counts
)

# ============================================================
# 6. Display results
# ============================================================

print("\n" + "=" * 60)
print("COOKIE CATS — SAMPLE RATIO MISMATCH TEST")
print("=" * 60)

results = pd.DataFrame({
    "Observed": observed_counts,
    "Expected": expected_counts,
    "Observed_Percentage": observed_counts / total_players * 100
})

print("\n1. Experimental Group Allocation:")
print(results.to_string())

print("\n2. Statistical Test Results:")
print(f"Chi-Square Statistic: {chi2_statistic:.6f}")
print(f"P-value: {p_value:.8f}")
print(f"Significance Level: {ALPHA}")

# ============================================================
# 7. Interpret the results
# ============================================================

print("\n3. Interpretation:")

if p_value < ALPHA:
    print(
        "WARNING: Potential sample ratio mismatch detected.\n"
        "The observed group allocation differs significantly "
        "from the expected 50/50 split.\n"
        "Investigate randomisation and data collection before "
        "interpreting the A/B test results."
    )
else:
    print(
        "No statistically significant sample ratio mismatch detected.\n"
        "The observed allocation is consistent with the "
        "expected 50/50 split at the selected significance level.\n"
        "This does not prove randomisation was implemented correctly."
    )

print("\n" + "=" * 60)
print("SRM TEST COMPLETED")
print("=" * 60)
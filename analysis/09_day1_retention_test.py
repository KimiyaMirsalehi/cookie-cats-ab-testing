import pandas as pd

from pathlib import Path
from statsmodels.stats.proportion import (
    proportions_ztest,
    confint_proportions_2indep
)

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
# 3. Experiment settings
# ============================================================

ALPHA = 0.05

CONTROL = "gate_30"
TREATMENT = "gate_40"

METRIC = "retention_1"

# ============================================================
# 4. Calculate retention statistics
# ============================================================

summary = (
    df.groupby("version")[METRIC]
    .agg(
        retained="sum",
        total="count",
        retention_rate="mean"
    )
)

control = summary.loc[CONTROL]
treatment = summary.loc[TREATMENT]

control_retained = int(control["retained"])
treatment_retained = int(treatment["retained"])

control_total = int(control["total"])
treatment_total = int(treatment["total"])

control_rate = control_retained / control_total
treatment_rate = treatment_retained / treatment_total

absolute_difference = treatment_rate - control_rate

relative_difference = (
    absolute_difference / control_rate * 100
)

# ============================================================
# 5. Two-sided hypothesis test
# ============================================================

counts = [treatment_retained, control_retained]
sample_sizes = [treatment_total, control_total]

z_statistic, p_value = proportions_ztest(
    count=counts,
    nobs=sample_sizes,
    alternative="two-sided"
)

# ============================================================
# 6. Confidence interval
# ============================================================

ci_lower, ci_upper = confint_proportions_2indep(
    count1=treatment_retained,
    nobs1=treatment_total,
    count2=control_retained,
    nobs2=control_total,
    compare="diff",
    method="newcomb",
    alpha=ALPHA
)

# ============================================================
# 7. Display results
# ============================================================

print("\n" + "=" * 65)
print("COOKIE CATS — DAY 1 RETENTION ANALYSIS")
print("=" * 65)

print("\n1. Group Statistics:")
print(summary.to_string(float_format=lambda x: f"{x:.6f}"))

print("\n2. Observed Difference:")

print(f"Control retention: {control_rate * 100:.3f}%")
print(f"Treatment retention: {treatment_rate * 100:.3f}%")

print(
    f"Absolute difference: "
    f"{absolute_difference * 100:+.3f} percentage points"
)

print(f"Relative difference: {relative_difference:+.2f}%")

print("\n3. Two-Sided Z-Test:")

print(f"Z-statistic: {z_statistic:.6f}")
print(f"P-value: {p_value:.8f}")

if p_value < ALPHA:
    print(
        "Result: Statistically significant difference "
        "in Day 1 retention."
    )
else:
    print(
        "Result: No statistically significant difference "
        "in Day 1 retention at the 5% level."
    )

print("\n4. 95% Confidence Interval:")

print(
    f"Lower bound: {ci_lower * 100:+.3f} percentage points"
)

print(
    f"Upper bound: {ci_upper * 100:+.3f} percentage points"
)

print("\n5. Interpretation:")

if ci_upper < 0:
    print(
        "The confidence interval is entirely negative, "
        "suggesting lower Day 1 retention for Gate 40."
    )
elif ci_lower > 0:
    print(
        "The confidence interval is entirely positive, "
        "suggesting higher Day 1 retention for Gate 40."
    )
else:
    print(
        "The confidence interval includes zero. "
        "The observed difference is not statistically "
        "significant at the 5% level."
    )

print("\nNote: This is an exploratory secondary-metric analysis.")

print("\n" + "=" * 65)
print("DAY 1 RETENTION TEST COMPLETED")
print("=" * 65)
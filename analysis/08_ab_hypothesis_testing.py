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
# 2. Load the dataset
# ============================================================

df = pd.read_csv(DATA_PATH)

# ============================================================
# 3. Define experiment settings
# ============================================================

ALPHA = 0.05

CONTROL = "gate_30"
TREATMENT = "gate_40"

PRIMARY_METRIC = "retention_7"

# ============================================================
# 4. Calculate group-level statistics
# ============================================================

summary = (
    df.groupby("version")[PRIMARY_METRIC]
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

# Treatment minus control
absolute_difference = treatment_rate - control_rate

relative_difference = (
    absolute_difference / control_rate * 100
)

# ============================================================
# 5. Primary hypothesis test — One-sided
# ============================================================

# Order matters: treatment first, control second
counts = [treatment_retained, control_retained]
sample_sizes = [treatment_total, control_total]

z_stat_one_sided, p_value_one_sided = proportions_ztest(
    count=counts,
    nobs=sample_sizes,
    alternative="larger"
)

# ============================================================
# 6. Supplementary hypothesis test — Two-sided
# ============================================================

z_stat_two_sided, p_value_two_sided = proportions_ztest(
    count=counts,
    nobs=sample_sizes,
    alternative="two-sided"
)

# ============================================================
# 7. Calculate 95% confidence interval
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
# 8. Display results
# ============================================================

print("\n" + "=" * 65)
print("COOKIE CATS — A/B HYPOTHESIS TESTING")
print("=" * 65)

print("\n1. Experiment Summary:")

print(
    summary.to_string(
        float_format=lambda x: f"{x:.6f}"
    )
)

print("\n2. Observed Treatment Effect:")

print(f"Control retention: {control_rate * 100:.3f}%")
print(f"Treatment retention: {treatment_rate * 100:.3f}%")

print(
    f"Absolute difference: "
    f"{absolute_difference * 100:+.3f} percentage points"
)

print(f"Relative difference: {relative_difference:+.2f}%")

print("\n3. Primary One-Sided Z-Test:")

print(f"Z-statistic: {z_stat_one_sided:.6f}")
print(f"P-value: {p_value_one_sided:.8f}")

if p_value_one_sided < ALPHA:
    print(
        "Decision: Reject H0.\n"
        "Statistically significant evidence that moving "
        "the gate to Level 40 improves Day 7 retention."
    )
else:
    print(
        "Decision: Fail to reject H0.\n"
        "Insufficient statistical evidence that moving "
        "the gate to Level 40 improves Day 7 retention."
    )

print("\n4. Supplementary Two-Sided Z-Test:")

print(f"Z-statistic: {z_stat_two_sided:.6f}")
print(f"P-value: {p_value_two_sided:.8f}")

if p_value_two_sided < ALPHA:
    print(
        "Decision: Reject H0.\n"
        "Evidence of a difference in Day 7 retention "
        "between the experimental groups."
    )
else:
    print(
        "Decision: Fail to reject H0.\n"
        "Insufficient evidence of a difference "
        "between the experimental groups."
    )

print("\n5. 95% Confidence Interval:")

print(
    f"Lower bound: {ci_lower * 100:+.3f} percentage points"
)

print(
    f"Upper bound: {ci_upper * 100:+.3f} percentage points"
)

print("\n6. Confidence Interval Interpretation:")

if ci_upper < 0:
    print(
        "The entire interval is below zero, "
        "indicating lower Day 7 retention for Gate 40."
    )
elif ci_lower > 0:
    print(
        "The entire interval is above zero, "
        "indicating higher Day 7 retention for Gate 40."
    )
else:
    print(
        "The interval includes zero, so the data "
        "are compatible with no difference."
    )

print("\n" + "=" * 65)
print("A/B HYPOTHESIS TESTING COMPLETED")
print("=" * 65)
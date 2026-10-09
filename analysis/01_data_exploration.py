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
# 3. Initial data inspection
# ============================================================

print("\n" + "=" * 60)
print("COOKIE CATS — DATA EXPLORATION & QUALITY ASSESSMENT")
print("=" * 60)

print("\n1. Dataset Shape:")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\n2. Column Names:")
print(df.columns.tolist())

print("\n3. First Five Rows:")
print(df.head())

print("\n4. Data Types:")
print(df.dtypes)

# ============================================================
# 4. Missing value assessment
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY CHECKS")
print("=" * 60)

print("\n5. Missing Values:")

missing_values = pd.DataFrame({
    "Missing_Count": df.isna().sum(),
    "Missing_Percentage": df.isna().mean() * 100
})

print(missing_values)

# ============================================================
# 5. Duplicate player assessment
# ============================================================

print("\n6. Duplicate Player IDs:")

duplicate_count = df["userid"].duplicated().sum()

print(f"Number of duplicate player IDs: {duplicate_count:,}")

# ============================================================
# 6. Experimental group distribution
# ============================================================

print("\n7. Experimental Group Distribution:")

group_distribution = (
    df["version"]
    .value_counts()
    .rename_axis("Version")
    .reset_index(name="Number_of_Players")
)

group_distribution["Percentage"] = (
    group_distribution["Number_of_Players"] / len(df) * 100
)

print(group_distribution.to_string(index=False))

# ============================================================
# 7. Validate game rounds
# ============================================================

print("\n8. Game Rounds Validation:")

negative_rounds = (df["sum_gamerounds"] < 0).sum()

zero_rounds = (df["sum_gamerounds"] == 0).sum()

print(f"Players with negative game rounds: {negative_rounds:,}")
print(f"Players with zero game rounds: {zero_rounds:,}")

# ============================================================
# 8. Validate experimental groups
# ============================================================

print("\n9. Experimental Group Validation:")

expected_groups = {"gate_30", "gate_40"}

actual_groups = set(df["version"].dropna().unique())

unexpected_groups = actual_groups - expected_groups

print(f"Groups identified: {sorted(actual_groups)}")
print(f"Unexpected groups: {sorted(unexpected_groups)}")

# ============================================================
# 9. Validate retention indicators
# ============================================================

print("\n10. Retention Indicator Validation:")

for column in ["retention_1", "retention_7"]:

    print(f"\n{column}:")

    print(df[column].value_counts(dropna=False))

    invalid_values = ~df[column].isin([True, False])

    print(f"Invalid values: {invalid_values.sum():,}")

# ============================================================
# 10. Summary
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY ASSESSMENT COMPLETED")
print("=" * 60)
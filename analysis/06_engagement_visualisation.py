import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

# ============================================================
# 1. Define project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "cookie_cats.csv"

OUTPUT_DIR = BASE_DIR / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 2. Load dataset
# ============================================================

df = pd.read_csv(DATA_PATH)

# ============================================================
# 3. Full distribution histogram
# ============================================================

fig, ax = plt.subplots(figsize=(11, 6))

ax.hist(
    df["sum_gamerounds"],
    bins=100,
    color="#4472C4",
    edgecolor="white"
)

ax.set_title(
    "Cookie Cats — Distribution of Game Rounds (All Players)",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Total Game Rounds")
ax.set_ylabel("Number of Players")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

full_path = OUTPUT_DIR / "engagement_distribution_full.png"

plt.savefig(full_path, dpi=300, bbox_inches="tight")
plt.close()

# ============================================================
# 4. Zoomed distribution by experimental group
# ============================================================

fig, ax = plt.subplots(figsize=(11, 6))

colors = {
    "gate_30": "#4472C4",
    "gate_40": "#ED7D31"
}

for version in ["gate_30", "gate_40"]:

    group_data = df.loc[
        df["version"] == version,
        "sum_gamerounds"
    ]

    ax.hist(
        group_data,
        bins=50,
        range=(0, 500),
        density=True,
        alpha=0.5,
        label=version,
        color=colors[version]
    )

ax.set_title(
    "Cookie Cats — Game Rounds Distribution by Group (0–500)",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Total Game Rounds")
ax.set_ylabel("Probability Density")

ax.legend(title="Experimental Group")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

zoomed_path = OUTPUT_DIR / "engagement_distribution_zoomed.png"

plt.savefig(zoomed_path, dpi=300, bbox_inches="tight")
plt.close()

# ============================================================
# 5. Print summary
# ============================================================

print("\n" + "=" * 60)
print("COOKIE CATS — ENGAGEMENT VISUALISATION")
print("=" * 60)

print("\nCharts saved successfully:")
print(full_path)
print(zoomed_path)

print("\nPercentage of players above 500 rounds:")

for version in ["gate_30", "gate_40"]:

    group_data = df.loc[
        df["version"] == version,
        "sum_gamerounds"
    ]

    percentage = (group_data > 500).mean() * 100

    print(f"{version}: {percentage:.2f}%")

print("\nENGAGEMENT VISUALISATION COMPLETED")
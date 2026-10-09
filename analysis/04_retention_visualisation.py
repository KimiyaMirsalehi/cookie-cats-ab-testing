import pandas as pd
import numpy as np
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
# 3. Calculate retention rates by experimental group
# ============================================================

retention = (
    df.groupby("version")[["retention_1", "retention_7"]]
    .mean()
    .mul(100)
    .reindex(["gate_30", "gate_40"])
)

# ============================================================
# 4. Prepare chart data
# ============================================================

groups = ["Gate 30 (Control)", "Gate 40 (Treatment)"]

day1 = retention["retention_1"].to_numpy()
day7 = retention["retention_7"].to_numpy()

x = np.arange(len(groups))
width = 0.32

# ============================================================
# 5. Create bar chart
# ============================================================

fig, ax = plt.subplots(figsize=(10, 6))

bars_day1 = ax.bar(
    x - width / 2,
    day1,
    width,
    label="Day 1 Retention",
    color="#4472C4"
)

bars_day7 = ax.bar(
    x + width / 2,
    day7,
    width,
    label="Day 7 Retention",
    color="#ED7D31"
)

# ============================================================
# 6. Format chart
# ============================================================

ax.set_title(
    "Cookie Cats — Player Retention by Experiment Group",
    fontsize=15,
    fontweight="bold",
    pad=20
)

ax.set_ylabel("Retention Rate (%)", fontsize=11)

ax.set_xticks(x)
ax.set_xticklabels(groups)

ax.set_ylim(0, 55)

ax.legend(frameon=False)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

# Add percentage labels
for bars in [bars_day1, bars_day7]:
    for bar in bars:
        height = bar.get_height()

        ax.annotate(
            f"{height:.2f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10
        )

# ============================================================
# 7. Save chart
# ============================================================

plt.tight_layout()

output_path = OUTPUT_DIR / "retention_comparison.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("\n" + "=" * 60)
print("COOKIE CATS — RETENTION VISUALISATION")
print("=" * 60)

print(f"\nChart saved successfully to:\n{output_path}")

print("\nRetention rates:")
print(retention.round(3))

plt.show()
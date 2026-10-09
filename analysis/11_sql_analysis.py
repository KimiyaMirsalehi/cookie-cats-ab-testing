import pandas as pd
import duckdb

from pathlib import Path

# ============================================================
# 1. Define project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "cookie_cats.csv"

SQL_DIR = BASE_DIR / "sql"

# ============================================================
# 2. Load dataset
# ============================================================

df = pd.read_csv(DATA_PATH)

# ============================================================
# 3. Create DuckDB connection
# ============================================================

con = duckdb.connect(database=":memory:")

con.register("players", df)

# ============================================================
# 4. Define SQL queries
# ============================================================

sql_files = {
    "Experimental Group Distribution": "01_experiment_groups.sql",
    "Player Retention Analysis": "02_retention_analysis.sql",
    "Player Engagement Analysis": "03_engagement_analysis.sql"
}

# ============================================================
# 5. Execute SQL queries
# ============================================================

print("\n" + "=" * 65)
print("COOKIE CATS — SQL ANALYTICS")
print("=" * 65)

try:
    for analysis_name, file_name in sql_files.items():

        sql_path = SQL_DIR / file_name

        sql_query = sql_path.read_text(encoding="utf-8")

        results = con.execute(sql_query).df()

        print(f"\n{analysis_name}:")
        print(results.to_string(index=False))

finally:
    con.close()

print("\n" + "=" * 65)
print("SQL ANALYSIS COMPLETED")
print("=" * 65)
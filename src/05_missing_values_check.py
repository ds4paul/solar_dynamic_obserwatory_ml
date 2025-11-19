# """
# 05_missing_values_check.py
#
# Cel:
# Analiza brakujących wartości (missing values) w datasetach po walidacji czasowej.
# Skrypt generuje:
# - zestawienie braków (per kolumna),
# - analizę procentową,
# - identyfikację kolon problematycznych,
# - zapisuje raport .md oraz tabelę .csv do teczki processed.
#
# Jest to krok przygotowujący do:
# 06_eda.py, 07_feature_engineering.py oraz later modelling steps.
# """
#
# import pandas as pd
# # from pathlib import Path
# from src.config import PROCESSED_DIR
#
# # === 1. PATHS ===
# INPUT_FILE = PROCESSED_DIR / "merged_xy_temporally_valid.csv"
# REPORT_FILE = PROCESSED_DIR / "missing_values_report.md"
# TABLE_FILE = PROCESSED_DIR / "missing_values_table.csv"
#
# print("[INFO] Loading validated dataset...")
# df = pd.read_csv(INPUT_FILE)
#
# print("[INFO] Dataset shape:", df.shape)
#
#
# # === 2. Missing values summary ===
# print("[INFO] Computing missing values table...")
#
# missing_counts = df.isna().sum()
# missing_percent = (df.isna().mean() * 100).round(3)
#
# missing_table = pd.DataFrame({
#     "missing_count": missing_counts,
#     "missing_percent": missing_percent
# }).sort_values("missing_percent", ascending=False)
#
# # Save table to CSV
# missing_table.to_csv(TABLE_FILE)
# print(f"[SAVED] Missing value table saved to: {TABLE_FILE}")
#
#
# # === 3. Basic reasoning ===
#
# # Identify columns with ANY missing values
# cols_with_missing = missing_table[missing_table["missing_count"] > 0]
#
# # Identify severe missing issues (>30%)
# severe_missing = missing_table[missing_table["missing_percent"] > 30]
#
# # Identify moderate missing issues (5%–30%)
# moderate_missing = missing_table[
#     (missing_table["missing_percent"] > 5) &
#     (missing_table["missing_percent"] <= 30)
# ]
#
# # Identify light missing issues (<5%)
# light_missing = missing_table[
#     (missing_table["missing_percent"] > 0) &
#     (missing_table["missing_percent"] <= 5)
# ]
#
#
# # === 4. Generate Markdown report ===
#
# print("[INFO] Creating missing value report...")
#
# with open(REPORT_FILE, "w") as f:
#     f.write("# Missing Values Report\n\n")
#     f.write("## Dataset shape\n")
#     f.write(f"- Rows: {df.shape[0]}\n")
#     f.write(f"- Columns: {df.shape[1]}\n\n")
#
#     f.write("## Global Missing Summary\n")
#     total_missing = missing_counts.sum()
#     f.write(f"- Total missing values: **{total_missing}**\n")
#     f.write(f"- Percentage of missing cells: "
#             f"**{(total_missing / (df.size) * 100):.3f}%**\n\n")
#
#     f.write("## Columns with missing values\n")
#     f.write(cols_with_missing.to_string())
#     f.write("\n\n")
#
#     f.write("## Severe missing issues (>30%)\n")
#     if severe_missing.empty:
#         f.write("✔ No severe missing issues.\n\n")
#     else:
#         f.write(severe_missing.to_string())
#         f.write("\n\n")
#
#     f.write("## Moderate missing issues (5%–30%)\n")
#     if moderate_missing.empty:
#         f.write("✔ No moderate missing issues.\n\n")
#     else:
#         f.write(moderate_missing.to_string())
#         f.write("\n\n")
#
#     f.write("## Light missing issues (<5%)\n")
#     if light_missing.empty:
#         f.write("✔ No light missing issues.\n\n")
#     else:
#         f.write(light_missing.to_string())
#         f.write("\n\n")
#
#     f.write("---\nGenerated automatically by 05_missing_values_check.py\n")
#
# print(f"[SAVED] Missing values report saved to: {REPORT_FILE}")
#
# print("\n[DONE] Missing value analysis completed.\n")
# print(missing_table.head(15))

"""
05_missing_values_check.py

Cel:
Analiza brakujących wartości w datasetach po walidacji czasowej.
Skrypt generuje:
- tabelę braków (CSV),
- raport .md,
- klasyfikację kolumn wg źródła (SDO / GOES / LABEL / TECH),
- klasyfikację poziomu braków (severe / moderate / light),
i przygotowuje dane do kroku 06 (EDA).
"""

import pandas as pd
from src.config import PROCESSED_DIR

# === 1. PATHS ===
INPUT_FILE = PROCESSED_DIR / "merged_xy_temporally_valid.csv"
REPORT_FILE = PROCESSED_DIR / "missing_values_report.md"
TABLE_FILE = PROCESSED_DIR / "missing_values_table.csv"

print("[INFO] Loading validated dataset...")
df = pd.read_csv(INPUT_FILE)

print("[INFO] Dataset shape:", df.shape)

# === 2. Missing values summary ===
missing_counts = df.isna().sum()
missing_percent = (df.isna().mean() * 100).round(3)

missing_table = pd.DataFrame({
    "missing_count": missing_counts,
    "missing_percent": missing_percent
}).sort_values("missing_percent", ascending=False)

missing_table.to_csv(TABLE_FILE)
print(f"[SAVED] Missing value table saved to: {TABLE_FILE}")

# === 3. Column source classification ===
SDO_COLS = [
    "HARP_NUM","T_REC_DATETIME",
    "USFLUX","MEANGAM","MEANGBT","MEANGBZ","MEANGBH",
    "MEANJZD","TOTUSJZ","MEANALP","MEANJZH","TOTUSJH",
    "ABSNJZH","SAVNCPP","MEANPOT","TOTPOT","MEANSHR",
    "SHRGT45","R_VALUE","GWILL"
]

GOES_COLS = [
    "start_datetime","end_datetime","peak_datetime","xray_class",
    "xray_intensity","latitude","longtitude","noaa_ar","source",
    "deeps_flare_id","delta_hours"
]

LABEL_COLS = [
    "now_flare_level","now_flare_id",
    "h6_flare_level","h6_flare_id",
    "h12_flare_level","h12_flare_id",
    "h24_flare_level","h24_flare_id",
    "h48_flare_level","h48_flare_id",
    "h24_posmx","h24_poscmx","h48_posmx","h48_poscmx",
    "h24_delta05","h48_delta05"
]

TECH_COLS = [
    "harpnum_trec","t_rec_str",
    "valid_now","valid_6h","valid_12h","valid_24h","valid_48h",
    "temporal_valid"
]

def get_source(col):
    if col in SDO_COLS:
        return "SDO"
    if col in GOES_COLS:
        return "GOES"
    if col in LABEL_COLS:
        return "LABEL"
    if col in TECH_COLS:
        return "TECH"
    return "OTHER"

missing_table["source"] = missing_table.index.map(get_source)

# === 4. Group missing levels ===
severe_missing = missing_table[missing_table["missing_percent"] > 80]
high_missing   = missing_table[(missing_table["missing_percent"] > 30) & (missing_table["missing_percent"] <= 80)]
moderate_missing = missing_table[(missing_table["missing_percent"] > 5) & (missing_table["missing_percent"] <= 30)]
light_missing = missing_table[(missing_table["missing_percent"] > 0) & (missing_table["missing_percent"] <= 5)]

# === 5. Generate markdown report ===
with open(REPORT_FILE, "w") as f:

    f.write("# Missing Values Report\n\n")
    f.write(f"Rows: **{df.shape[0]}**, Columns: **{df.shape[1]}**\n\n")

    total_missing = missing_counts.sum()
    f.write(f"- Total missing values: **{total_missing}**\n")
    f.write(f"- Global percentage missing: **{(total_missing / df.size * 100):.3f}%**\n\n")

    f.write("## Severe missing (>80%) \n")
    f.write(severe_missing.to_string() if not severe_missing.empty else "✔ None\n")
    f.write("\n\n")

    f.write("## High missing (30%–80%) ️\n")
    f.write(high_missing.to_string() if not high_missing.empty else "✔ None\n")
    f.write("\n\n")

    f.write("## Moderate missing (5%–30%) \n")
    f.write(moderate_missing.to_string() if not moderate_missing.empty else "✔ None\n")
    f.write("\n\n")

    f.write("## Light missing (<5%) \n")
    f.write(light_missing.to_string() if not light_missing.empty else "✔ None\n")
    f.write("\n\n")

    f.write("## Full missing table\n")
    f.write(missing_table.to_string())
    f.write("\n\n---\nGenerated automatically by 05_missing_values_check.py\n")

print(f"[SAVED] Missing values report saved to: {REPORT_FILE}")
print("[DONE] Missing value analysis completed.")


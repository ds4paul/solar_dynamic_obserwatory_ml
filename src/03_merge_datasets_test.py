"""
03_merge_datasets_test.py

This script performs a temporary (test-stage) merge of three data sources:

1 selected_features.csv      - physical SHARP magnetic features (SDO/HMI) used as ML inputs (X)
2 nlfff_flare_label.csv      - predictive label dataset (y) for supervised learning
3 flare_info.csv             - GOES flare event catalog used ONLY for validation (NOT features)

Important notes:
- Successful merging requires identical column names used as join keys.
- In raw datasets, key columns differ in case sensitivity:
      * SDO dataset uses:        "HARP_NUM"
      * Label dataset uses:      "harp_num"
  Therefore, we standardize and normalize merge keys to uppercase for reliability.
"""

import pandas as pd
from src.config import INTERIM_DIR, CSV_LABEL, CSV_INFO

# Load selected SHARP features (input X)
X_PATH = INTERIM_DIR / "selected_features.csv"
df_X = pd.read_csv(X_PATH)

# Load ML label dataset (target y)
df_label = pd.read_csv(CSV_LABEL)

# Load GOES flare information for validation
df_info = pd.read_csv(CSV_INFO)

print("\n[INFO] Loaded dataset shapes:")
print(f"X (selected_features.csv): {df_X.shape}")
print(f"Labels (nlfff_flare_label.csv): {df_label.shape}")
print(f"GOES (flare_info.csv): {df_info.shape}")


# 1 NORMALIZE COLUMN NAMES (EXPLANATION)

# Pandas merge requires column names to match EXACTLY.
# "harp_num" and "HARP_NUM" are treated as two different columns.
# To avoid merge errors, we rename label dataset columns to match X dataset.


df_label = df_label.rename(columns={
    "harp_num": "HARP_NUM",
    "t_rec_datetime": "T_REC_DATETIME"
})

print("\nMerge key column names normalized.")

# 2 MERGE FEATURES (X) WITH LABELS (y)


merge_keys = ["HARP_NUM", "T_REC_DATETIME"]
df_xy = df_X.merge(df_label, on=merge_keys, how="inner")
print(f"[OK] X + y merged shape: {df_xy.shape}")



# GOES records are NOT linked using HARP_NUM (different institutions + different IDs).
# Instead, we align by timestamp using merge_asof, allowing a time tolerance window.


# Convert datetime fields
df_xy["T_REC_DATETIME"] = pd.to_datetime(df_xy["T_REC_DATETIME"])
df_info["peak_datetime"] = pd.to_datetime(df_info["peak_datetime"], errors="coerce")

# Remove missing datetime entries
df_xy = df_xy.dropna(subset=["T_REC_DATETIME"])
df_info = df_info.dropna(subset=["peak_datetime"])

# Sorting is required for merge_asof
df_xy = df_xy.sort_values("T_REC_DATETIME")
df_info = df_info.sort_values("peak_datetime")

# Perform tolerance-based merge (2-hour window)
df_final = pd.merge_asof(
    df_xy,
    df_info,
    left_on="T_REC_DATETIME",
    right_on="peak_datetime",
    direction="forward",
    tolerance=pd.Timedelta("2h")
)

print(f"[OK] Final merged dataset shape (X + y + GOES): {df_final.shape}")

# Calculate time-match percentage
match_rate = df_final["peak_datetime"].notna().mean() * 100
print(f"[INFO] GOES timestamp match rate: {match_rate:.2f}%")

# 4 SAVE TEMPORARY MERGED OUTPUT

OUT_PATH = INTERIM_DIR / "merged_xy_goes_test.csv"
df_final.to_csv(OUT_PATH, index=False)

print(f"\n[SAVED] Test merged dataset saved to:\n{OUT_PATH}")
print("[NOTE] This output is TEMPORARY — final dataset will be validated and cleaned later.")

# NEXT STEP: TEMPORAL VALIDATION (to be done in next script)

# This merge test only verifies that:
#   - Key columns can be aligned
#   - Datetime formats are consistent
#   - Basic tolerance-based timestamp matching works

# However, this script does NOT yet confirm:
#   * temporal causality  (feature_time < flare_time)
#   * lack of information leakage
#   * correct prediction horizon assignment (now / 6h / 12h / 24h / 48h)
#   * physical interpretability / data sanity

# These checks will be implemented in the next module:
#   04_temporal_validation.py (new file)

# In that script we will:
#   1. Ensure features come strictly BEFORE flare occurrence
#   2. Verify matching window logic and shift alignment
#   3. Validate flare horizon labels:
#          T_REC_DATETIME < peak_datetime <= T_REC + horizon
#   4. Detect and report invalid, duplicated, or conflicting matches

# Only after confirming temporal integrity,
# final training dataset will be generated in:
#   data/processed/final_training_set.csv


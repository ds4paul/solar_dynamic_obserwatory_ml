import pandas as pd
from src.config import INTERIM_DIR, CSV_LABEL


# === 1. LOAD INPUT FILES ===
X_PATH = INTERIM_DIR / "selected_features.csv"
df_X = pd.read_csv(X_PATH)

df_label = pd.read_csv(CSV_LABEL)

print("[INFO] Loaded shapes:")
print("SDO features (X):", df_X.shape)
print("NLFFF labels (y):", df_label.shape)


# === 2. NORMALIZE COLUMN NAMES ===
# W label dataset kolumny mają małe litery — ujednolicamy.
df_label = df_label.rename(columns={
    "harp_num": "HARP_NUM",
    "t_rec_datetime": "T_REC_DATETIME"
})


# === 3. MERGE SDO FEATURES WITH LABEL DATA ===
merge_keys = ["HARP_NUM", "T_REC_DATETIME"]

df_merged = df_X.merge(df_label, on=merge_keys, how="inner")

print("[OK] Merged SDO + labels:", df_merged.shape)


# === 4. SAVE CLEAN MERGED OUTPUT ===
OUT_PATH = INTERIM_DIR / "merged_xy_clean.csv"
df_merged.to_csv(OUT_PATH, index=False)

print(f"[SAVED] Clean merged dataset saved to:\n{OUT_PATH}")
print("[DONE] This dataset is ready for temporal validation (step 04).")
"""
02_select_features.py
----------------------

This script performs feature selection ONLY on the SDO/HMI magnetic dataset
(`nlfff_raw.csv`) because it contains the input features (X) used for machine
learning modeling. We keep only physically meaningful and causal SHARP magnetic
parameters together with join keys required for later merging.

The label dataset (`nlfff_flare_label.csv`) and the validation dataset
(`flare_info.csv`) are NOT modified in this step, since they contain target values
and real flare outcomes rather than input features.

Steps performed in this script:
1. Load raw SHARP magnetic dataset (`nlfff_raw.csv`)
2. Select physical magnetic features + necessary join keys
3. Save reduced dataset to `data/interim/selected_features.csv`
4. Remove large original raw CSV file to avoid storage overload and GitHub size limits
"""

import os
import pandas as pd
from config import CSV_RAW, INTERIM_DIR

def select_features():
    print('Loading RAW dataset...')
    df_raw = pd.read_csv(CSV_RAW)

    # Required columns for merging
    KEY_COLUMNS = ["HARP_NUM", "T_REC_DATETIME"]

    # Physical magnetic SHARP features
    PHYSICAL_FEATURES = [
        "USFLUX", "MEANGAM", "MEANGBT", "MEANGBZ", "MEANGBH",
        "MEANJZD", "TOTUSJZ", "MEANALP", "MEANJZH", "TOTUSJH",
        "ABSNJZH", "SAVNCPP", "MEANPOT", "TOTPOT", "MEANSHR",
        "SHRGT45", "R_VALUE", "GWILL"
    ]

    SELECTED_COLS = KEY_COLUMNS + PHYSICAL_FEATURES

    print('Saving selected features...')
    df_selected = df_raw[SELECTED_COLS].copy()

    output_path = INTERIM_DIR / "selected_features.csv"
    df_selected.to_csv(output_path, index=False)

    print(f"Saved file: {output_path}")
    print(f"Final selected features: {df_selected.shape}")

    # Remove heavy original raw file
    try:
        os.remove(CSV_RAW)
        print(f"Deleted heavy raw file: {CSV_RAW}")
    except Exception as e:
        print(f"[WARNING] Could not delete raw dataset: {e}")

    return df_selected


if __name__ == "__main__":
    select_features()
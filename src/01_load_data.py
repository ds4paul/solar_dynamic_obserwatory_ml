"""
01_load_data.py
Loads raw CSV files into pandas DataFrames and prints basic metadata.
"""

import pandas as pd
from config import CSV_RAW, CSV_LABEL, CSV_INFO

def load_csv_files():
    """Load raw CSV files into pandas DataFrames."""
    df_raw = pd.read_csv(CSV_RAW)
    df_label = pd.read_csv(CSV_LABEL)
    df_info = pd.read_csv(CSV_INFO)
    return df_raw, df_label, df_info

if __name__ == "__main__":
    df_raw, df_label, df_info = load_csv_files()

    print("\n[INFO] Raw data loaded successfully.")
    print("------------------------------------")
    print(f"nlfff_raw.csv:          {df_raw.shape}")
    print(f"nlfff_flare_label.csv:  {df_label.shape}")
    print(f"flare_info.csv:         {df_info.shape}")

    # We do not explore full raw data here due to 276 columns
    print("\nFull raw dataset contains technical & metadata columns.")
    print("      Feature selection will be performed in 02_select_features.py")
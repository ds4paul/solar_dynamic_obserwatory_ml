import pandas as pd
from src.config import PROCESSED_DIR

df = pd.read_csv(PROCESSED_DIR / "merged_xy_temporally_valid.csv")

# 1. Wiersze, gdzie była flara
flare_rows = df[
    (df["now_flare_level"] > 0) |
    (df["h6_flare_level"] > 0) |
    (df["h12_flare_level"] > 0) |
    (df["h24_flare_level"] > 0) |
    (df["h48_flare_level"] > 0)
]

print("Liczba wierszy z flarami:", len(flare_rows))

# 2. Missing values w GOES tylko dla wierszy z flarami
goes_cols = [
    "start_datetime","end_datetime","peak_datetime",
    "xray_class","xray_intensity","latitude","longtitude",
    "noaa_ar","deeps_flare_id"
]

missing_in_flares = flare_rows[goes_cols].isna().sum().sort_values(ascending=False)
print("\nBraki w GOES TYLKO tam, gdzie była flara:\n")
print(missing_in_flares)

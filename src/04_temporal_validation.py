"""
04_temporal_validation.py

Cel:
Sprawdzić poprawność czasową (temporal causality) między:
- czasem pomiaru cech fizycznych SDO/HMI (T_REC_DATETIME)
- czasem wystąpienia flary GOES (peak_datetime)

Efekt:
- dodanie kolumny delta_hours
- dodanie flag poprawności dla każdego horyzontu (now/6/12/24/48)
- kolumna temporal_valid (True/False)
- raport markdown
- zapis przefiltrowanego datasetu
"""

import pandas as pd
from pathlib import Path
from src.config import INTERIM_DIR, PROCESSED_DIR

# === 1. Paths ===
INPUT_FILE = INTERIM_DIR / "merged_xy_goes_test.csv"
OUTPUT_FILE = PROCESSED_DIR / "merged_xy_temporally_valid.csv"
REPORT_FILE = PROCESSED_DIR / "temporal_validation_report.md"


# === 2. Load data ===
print("[INFO] Loading merged dataset...")
df = pd.read_csv(INPUT_FILE)

print("[INFO] Converting datetimes...")
df["T_REC_DATETIME"] = pd.to_datetime(df["T_REC_DATETIME"], utc=True, errors="coerce")
df["peak_datetime"] = pd.to_datetime(df["peak_datetime"], utc=True, errors="coerce")


# === 3. Compute time difference ===
print("[INFO] Computing delta_hours...")
df["delta_hours"] = (df["peak_datetime"] - df["T_REC_DATETIME"]) \
                        .dt.total_seconds() / 3600.0


# === 4. Horizon validation logic ===
def valid_window(delta, hours):
    return (delta > 0) & (delta <= hours)

print("[INFO] Checking horizon correctness...")

df["valid_now"]  = df["delta_hours"] >= 0
df["valid_6h"]   = valid_window(df["delta_hours"], 6)
df["valid_12h"]  = valid_window(df["delta_hours"], 12)
df["valid_24h"]  = valid_window(df["delta_hours"], 24)
df["valid_48h"]  = valid_window(df["delta_hours"], 48)


# === 5. Final temporal validity flag ===
df["temporal_valid"] = (
    df["valid_now"] &
    (
        df["valid_6h"] |
        df["valid_12h"] |
        df["valid_24h"] |
        df["valid_48h"]
    )
)


# === 6. Stats ===
summary = {
    "total_rows": len(df),
    "valid_rows": int(df["temporal_valid"].sum()),
    "invalid_rows": int((~df["temporal_valid"]).sum()),
    "valid_ratio": round(df["temporal_valid"].mean(), 4),
}

horizon_stats = pd.DataFrame({
    "valid_ratio": [
        df["valid_now"].mean(),
        df["valid_6h"].mean(),
        df["valid_12h"].mean(),
        df["valid_24h"].mean(),
        df["valid_48h"].mean(),
    ]
}, index=["now", "6h", "12h", "24h", "48h"]).round(4)


# === 7. Save output ===
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)
print(f"[SAVED] Temporally validated dataset saved to: {OUTPUT_FILE}")


# === 8. Save report ===
with open(REPORT_FILE, "w") as f:
    f.write("# Temporal Validation Report\n\n")
    f.write("## Summary\n")
    for k, v in summary.items():
        f.write(f"- **{k}**: {v}\n")

    f.write("\n## Horizon Validity\n")
    f.write(horizon_stats.to_string())
    f.write("\n\n---\nGenerated automatically by 04_temporal_validation.py\n")

print(f"[SAVED] Temporal validation report saved to: {REPORT_FILE}")


# === 9. Done ===
print("[DONE] Temporal validation complete.\n")
print(summary)
print("\nHorizon stats:\n", horizon_stats)

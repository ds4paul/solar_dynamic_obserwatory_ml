"""
shared constants for project
"""

from pathlib import Path

# base directories

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

# ensure directories exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# raw data file path

CSV_RAW = RAW_DIR / "nlfff_raw.csv"
CSV_LABEL = RAW_DIR / "nlfff_flare_label.csv"
CSV_INFO = RAW_DIR / "flare_info.csv"
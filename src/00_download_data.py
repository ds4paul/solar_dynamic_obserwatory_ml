from pathlib import Path
import gdown

# Setup project directories

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# File name and Google Drive IDs

files = {
    "flare_info.csv": "1LU4Js4fyA0Hl1fmAKjH7rSDzpfxD90r1",
    "nlfff_flare_label.csv": "1MRRVrNkP0UIONW9aGk1LUoeN2OcxlCKG",
    "nlfff_raw.csv": "19uYRjL3k-hy6aIV4g4QsHVcwyvcDyx0-",
}

# Downloads raw CSV files from Google Drive

for filename, file_id in files.items():
    url = f"https://drive.google.com/uc?id={file_id}"
    output_path = RAW_DIR / filename
    print(f"[INFO] Downloading {filename} -> {output_path}")
    gdown.download(url, str(output_path), quiet=False)

print("\n[OK] All raw data files downloaded successfully.")

# The downloaded files are large, so it's better not to commit them to GitHub right now.
# It's best to do it only after removing unnecessary data,
# because GitHub warns that the file exceeds 100 MB and after committing it
# I won't be able to push the changes.
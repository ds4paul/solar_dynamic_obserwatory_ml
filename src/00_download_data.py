"""
00_download_data.py
Download raw data from Google Drive into /data/raw directory.

Large raw files should NOT be committed to GitHub until preprocessing
reduces file size to meet GitHub limits (<100 MB).
"""

import gdown
from config import RAW_DIR

# Google Drive file ID

FILES = {
    "flare_info.csv": "1LU4Js4fyA0Hl1fmAKjH7rSDzpfxD90r1",
    "nlfff_flare_label.csv": "1MRRVrNkP0UIONW9aGk1LUoeN2OcxlCKG",
    "nlfff_raw.csv": "19uYRjL3k-hy6aIV4g4QsHVcwyvcDyx0-",
}

def download_raw_files():
    """Download all raw csv datasets."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for filename, file_id in FILES.items():
        url = f"https://drive.google.com/uc?id={file_id}"
        output_path = RAW_DIR / filename
        print(f"Downloading {filename} to {output_path}")
        gdown.download(url, str(output_path), quiet=False)

    print("Download complete.")

if __name__ == "__main__":
    download_raw_files()

    print(
        "\n[WARNING] Raw files are large. Do NOT commit them to GitHub until "
        "unnecessary columns are removed to stay under size limits."
    )
"""Download and verify the shared-bike dataset from Hugging Face."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import requests

DATASET_ID = "supersam7/bike_sharing"
REVISION = "main"
FILENAME = "bike_sharing.csv"
URL = f"https://huggingface.co/datasets/{DATASET_ID}/resolve/{REVISION}/{FILENAME}"
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def download() -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destination = RAW_DIR / FILENAME
    digest = hashlib.sha256()
    with requests.get(URL, timeout=60, stream=True) as response, destination.open("wb") as output:
        response.raise_for_status()
        for chunk in response.iter_content(1024 * 1024):
            if not chunk:
                continue
            output.write(chunk)
            digest.update(chunk)

    metadata = {
        "dataset_id": DATASET_ID,
        "revision": REVISION,
        "filename": FILENAME,
        "source_url": URL,
        "sha256": digest.hexdigest(),
        "bytes": destination.stat().st_size,
    }
    (RAW_DIR / "dataset_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Downloaded {destination} ({metadata['bytes']:,} bytes)")
    print(f"SHA-256: {metadata['sha256']}")
    return destination


if __name__ == "__main__":
    download()

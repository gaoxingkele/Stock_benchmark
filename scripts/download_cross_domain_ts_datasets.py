"""Download small registered cross-domain time-series datasets.

Only rows with download_status=planned are downloaded by default. Large
documented-only datasets stay as metadata until a focused reproduction needs
them.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "papers/metadata/lingxi_cross_domain_ts_datasets.csv"
PROFILE_OUT = ROOT / "data/external/time_series_sota/dataset_profile.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", default=str(DATASETS))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--retries", type=int, default=3)
    return parser.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def profile_csv(path: Path) -> dict[str, str]:
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = sum(1 for _ in reader)
    return {
        "rows": str(rows),
        "columns": str(len(header)),
        "header": ";".join(header),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
    }


def download_with_retries(url: str, target: Path, retries: int) -> None:
    tmp = target.with_suffix(target.suffix + ".tmp")
    for attempt in range(1, retries + 1):
        try:
            if tmp.exists():
                tmp.unlink()
            with urllib.request.urlopen(url, timeout=60) as response, tmp.open("wb") as file:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    file.write(chunk)
            tmp.replace(target)
            return
        except Exception as exc:  # noqa: BLE001
            if tmp.exists():
                tmp.unlink()
            if attempt >= retries:
                raise
            wait = 2 * attempt
            print(f"retry {attempt}/{retries} for {url}: {exc}; sleeping {wait}s")
            time.sleep(wait)


def main() -> int:
    args = parse_args()
    metadata = Path(args.metadata)
    profiles: list[dict[str, str]] = []
    with metadata.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if row["download_status"] != "planned":
                continue
            target = ROOT / row["local_target"]
            target.parent.mkdir(parents=True, exist_ok=True)
            if args.force or not target.exists():
                print(f"downloading {row['dataset_id']} -> {target}")
                download_with_retries(row["source_url"], target, args.retries)
            stats = profile_csv(target)
            profiles.append(
                {
                    "dataset_id": row["dataset_id"],
                    "name": row["name"],
                    "source_url": row["source_url"],
                    "local_path": row["local_target"],
                    **stats,
                }
            )

    PROFILE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with PROFILE_OUT.open("w", newline="", encoding="utf-8") as file:
        fields = ["dataset_id", "name", "source_url", "local_path", "rows", "columns", "header", "bytes", "sha256"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(profiles)
    print(f"profile={PROFILE_OUT} rows={len(profiles)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Validate raw Tushare dataset files before panel construction."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_FILES = ["trade_cal.csv", "stock_basic.csv", "index_weight.csv", "index_daily.csv", "daily.csv", "adj_factor.csv", "daily_basic.csv"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--allow-partial", action="store_true", help="Report missing open dates without failing.")
    return parser.parse_args()


def count_rows(path: Path) -> int:
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)
        return sum(1 for _ in reader)


def open_dates(path: Path) -> list[str]:
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return sorted(row["cal_date"] for row in reader if row.get("is_open") == "1")


def dates_in_file(path: Path, field: str = "trade_date") -> set[str]:
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return {row[field] for row in reader if row.get(field)}


def main() -> int:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    missing = [name for name in REQUIRED_FILES if not (raw_dir / name).exists()]
    if missing:
        raise RuntimeError(f"missing raw files: {', '.join(missing)}")

    counts = {name: count_rows(raw_dir / name) for name in REQUIRED_FILES}
    dates = open_dates(raw_dir / "trade_cal.csv")
    if not dates:
        raise RuntimeError("trade_cal.csv has no open dates")

    for name in ["daily.csv", "adj_factor.csv", "daily_basic.csv"]:
        available_dates = dates_in_file(raw_dir / name)
        missing_dates = [date for date in dates if date not in available_dates]
        if missing_dates and not args.allow_partial:
            raise RuntimeError(f"{name} missing {len(missing_dates)} open dates, first={missing_dates[:5]}")
        if missing_dates:
            print(f"{name}: missing_open_dates={len(missing_dates)} first_missing={missing_dates[:5]}")

    print(f"raw_dir={raw_dir}")
    print(f"open_dates={len(dates)} first={dates[0]} last={dates[-1]}")
    for name in REQUIRED_FILES:
        print(f"{name}: rows={counts[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

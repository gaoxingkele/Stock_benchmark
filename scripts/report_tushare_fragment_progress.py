"""Report per-date Tushare fragment download progress."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DATE_TABLES = ["daily", "adj_factor", "daily_basic"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", required=True)
    return parser.parse_args()


def open_dates(raw_dir: Path) -> list[str]:
    with (raw_dir / "trade_cal.csv").open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return sorted(row["cal_date"] for row in reader if row.get("is_open") == "1")


def fragment_dates(raw_dir: Path, api_name: str) -> set[str]:
    fragment_dir = raw_dir / "_fragments" / api_name
    if not fragment_dir.exists():
        return set()
    return {path.stem for path in fragment_dir.glob("*.csv") if path.stat().st_size > 0}


def main() -> int:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    dates = open_dates(raw_dir)
    expected = set(dates)
    by_table = {api_name: fragment_dates(raw_dir, api_name) for api_name in DATE_TABLES}
    complete_dates = set.intersection(*(by_table[api_name] for api_name in DATE_TABLES)) if by_table else set()

    print(f"raw_dir={raw_dir}")
    print(f"open_dates={len(dates)} first={dates[0] if dates else ''} last={dates[-1] if dates else ''}")
    for api_name in DATE_TABLES:
        done = by_table[api_name]
        missing = [date for date in dates if date not in done]
        print(
            f"{api_name}: fragments={len(done)} missing={len(expected - done)} "
            f"next_missing={missing[0] if missing else ''}"
        )
    missing_complete = [date for date in dates if date not in complete_dates]
    print(f"complete_date_triplets={len(complete_dates)} missing_complete={len(expected - complete_dates)}")
    print(f"next_incomplete_date={missing_complete[0] if missing_complete else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

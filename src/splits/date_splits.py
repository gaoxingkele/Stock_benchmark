"""Date-window utilities for daily benchmark panels."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DateSplit:
    name: str
    start_date: str
    end_date: str

    def contains(self, date: str) -> bool:
        return self.start_date <= date <= self.end_date


def read_calendar(path: str | Path) -> list[str]:
    with Path(path).open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def calendar_coverage(calendar: list[str], splits: list[DateSplit]) -> dict[str, int]:
    return {split.name: sum(1 for date in calendar if split.contains(date)) for split in splits}


def count_panel_rows_by_split(panel_path: str | Path, splits: list[DateSplit]) -> dict[str, int]:
    counts = {split.name: 0 for split in splits}
    with Path(panel_path).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row["date"]
            for split in splits:
                if split.contains(date):
                    counts[split.name] += 1
                    break
    return counts

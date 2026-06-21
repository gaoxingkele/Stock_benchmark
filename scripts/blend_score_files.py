"""Blend two per-stock score CSV files by daily z-scores."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left", required=True)
    parser.add_argument("--right", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--left-weight", type=float, default=0.75)
    parser.add_argument("--right-weight", type=float, default=0.25)
    return parser.parse_args()


def to_float(value: str | None) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def read_scores(path: Path) -> dict[tuple[str, str], dict[str, float | str]]:
    rows: dict[tuple[str, str], dict[str, float | str]] = {}
    with path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            score = to_float(row.get("score"))
            if math.isfinite(score):
                rows[(row["date"], row["symbol"])] = {"score": score, "label": row.get("label", "")}
    return rows


def daily_z(values: dict[tuple[str, str], float]) -> dict[tuple[str, str], float]:
    by_date: dict[str, list[tuple[tuple[str, str], float]]] = defaultdict(list)
    for key, value in values.items():
        by_date[key[0]].append((key, value))
    out: dict[tuple[str, str], float] = {}
    for pairs in by_date.values():
        arr = np.asarray([value for _, value in pairs], dtype=float)
        mean = float(np.mean(arr))
        std = float(np.std(arr))
        if std <= 1e-12:
            std = 1.0
        for key, value in pairs:
            out[key] = (value - mean) / std
    return out


def main() -> int:
    args = parse_args()
    left = read_scores(Path(args.left))
    right = read_scores(Path(args.right))
    keys = sorted(set(left) & set(right))
    left_z = daily_z({key: float(left[key]["score"]) for key in keys})
    right_z = daily_z({key: float(right[key]["score"]) for key in keys})
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "symbol", "score", "label"])
        writer.writeheader()
        for date, symbol in keys:
            score = args.left_weight * left_z[(date, symbol)] + args.right_weight * right_z[(date, symbol)]
            writer.writerow({"date": date, "symbol": symbol, "score": f"{score:.10f}", "label": left[(date, symbol)]["label"]})
    print(f"wrote {out} rows={len(keys)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

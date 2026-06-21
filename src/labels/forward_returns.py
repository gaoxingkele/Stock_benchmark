"""Forward-return label generation for benchmark panels."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def build_forward_return_labels(panel_path: str | Path, horizon: int = 1, price_field: str = "close") -> list[dict[str, str]]:
    if horizon <= 0:
        raise ValueError("horizon must be positive")

    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with Path(panel_path).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows_by_symbol[row["symbol"]].append(row)

    labels: list[dict[str, str]] = []
    for symbol, rows in sorted(rows_by_symbol.items()):
        rows = sorted(rows, key=lambda row: row["date"])
        for i, row in enumerate(rows):
            j = i + horizon
            if j >= len(rows):
                continue
            current_price = to_float(row[price_field])
            future_price = to_float(rows[j][price_field])
            if math.isnan(current_price) or math.isnan(future_price) or current_price <= 0:
                continue
            labels.append(
                {
                    "date": row["date"],
                    "symbol": symbol,
                    "ts_code": row.get("ts_code", ""),
                    "horizon": str(horizon),
                    "label": f"{future_price / current_price - 1.0:.10f}",
                }
            )
    labels.sort(key=lambda row: (row["date"], row["symbol"]))
    return labels


def write_labels(labels: list[dict[str, str]], out_path: str | Path) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "symbol", "ts_code", "horizon", "label"])
        writer.writeheader()
        writer.writerows(labels)

"""Minimal example: load data, evaluate factors, and print latest top 20 picks."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from evaluate_factors import evaluate_library


def main() -> None:
    # 1. Load your panel data (replace with your own path).
    data = pd.read_parquet("your_data.parquet")

    # 2. Load metadata.
    with open("expressions.json", "r", encoding="utf-8") as f:
        meta = json.load(f)

    # 3. Evaluate factors.
    signals = evaluate_library(data, meta["expressions"], meta["combined_signals"])

    # 4. Get latest date and rank by combined 5d signal.
    latest = signals.index.get_level_values("date").max()
    latest_signals = signals.xs(latest, level="date")["combined_5d"].dropna()
    top20 = latest_signals.sort_values(ascending=False).head(20)

    print(f"Top 20 picks on {latest.date()}:")
    print(top20.to_string())


if __name__ == "__main__":
    main()

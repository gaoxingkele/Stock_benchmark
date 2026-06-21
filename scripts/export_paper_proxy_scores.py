"""Export per-stock scores from the local paper-proxy models."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from run_trade_validation import fit_predictions  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--panel", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--lookback", type=int, default=20)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--valid-start", default="2022-01-04")
    parser.add_argument("--valid-end", default="2022-12-30")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2024-12-31")
    parser.add_argument("--ridge-alpha", type=float, default=10.0)
    parser.add_argument("--max-train-rows", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows, scores = fit_predictions(args, args.model)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "symbol", "score", "label"])
        writer.writeheader()
        for row, score in zip(rows, scores):
            writer.writerow(
                {
                    "date": row["date"],
                    "symbol": row["symbol"],
                    "score": f"{float(score):.10f}",
                    "label": f"{float(row['label']):.10f}",
                }
            )
    print(f"wrote {out} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

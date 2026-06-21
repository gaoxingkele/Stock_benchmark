"""Run a tiny factor IC/RankIC smoke test on a processed panel."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import pearson_corr, safe_ir, safe_mean, spearman_corr  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_smoke" / "panel.csv"))
    parser.add_argument("--score-field", default="pct_chg", help="Column used as the smoke prediction score.")
    parser.add_argument("--horizon", type=int, default=1, help="Forward return horizon in trading rows per symbol.")
    parser.add_argument("--out", default=str(PROJECT_ROOT / "experiments" / "baselines" / "factor_smoke_csi300.csv"))
    return parser.parse_args()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def main() -> int:
    args = parse_args()
    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with Path(args.panel).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows_by_symbol[row["symbol"]].append(row)

    scored_rows: list[dict[str, float | str]] = []
    for symbol, rows in rows_by_symbol.items():
        rows = sorted(rows, key=lambda row: row["date"])
        for i, row in enumerate(rows):
            j = i + args.horizon
            if j >= len(rows):
                continue
            close_now = to_float(row["close"])
            close_future = to_float(rows[j]["close"])
            score = to_float(row[args.score_field])
            if close_now <= 0 or math.isnan(score):
                continue
            label = close_future / close_now - 1.0
            scored_rows.append({"date": row["date"], "symbol": symbol, "score": score, "label": label})

    by_date: dict[str, list[dict[str, float | str]]] = defaultdict(list)
    for row in scored_rows:
        by_date[str(row["date"])].append(row)

    result_rows: list[dict[str, str]] = []
    ic_values: list[float] = []
    rankic_values: list[float] = []
    for date in sorted(by_date):
        day_rows = by_date[date]
        scores = [float(row["score"]) for row in day_rows]
        labels = [float(row["label"]) for row in day_rows]
        ic = pearson_corr(scores, labels)
        rankic = spearman_corr(scores, labels)
        ic_values.append(ic)
        rankic_values.append(rankic)
        result_rows.append(
            {
                "date": date,
                "n": str(len(day_rows)),
                "ic": f"{ic:.8f}",
                "rankic": f"{rankic:.8f}",
            }
        )

    summary = {
        "date": "SUMMARY",
        "n": str(len(scored_rows)),
        "ic": f"{safe_mean(ic_values):.8f}",
        "rankic": f"{safe_mean(rankic_values):.8f}",
        "icir": f"{safe_ir(ic_values):.8f}",
        "rankicir": f"{safe_ir(rankic_values):.8f}",
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["date", "n", "ic", "rankic", "icir", "rankicir"]
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in result_rows:
            writer.writerow({**{"icir": "", "rankicir": ""}, **row})
        writer.writerow(summary)

    print(f"rows={len(scored_rows)} dates={len(result_rows)} out={out_path}")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


"""Evaluate all factor columns against forward returns."""

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
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_by_date_smoke" / "panel.csv"))
    parser.add_argument("--factors", default=str(PROJECT_ROOT / "data" / "features" / "basic_factors" / "csi300_by_date_smoke.csv"))
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--out", default=str(PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_ic_csi300_by_date.csv"))
    return parser.parse_args()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def build_labels(panel_path: Path, horizon: int) -> dict[tuple[str, str], float]:
    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with panel_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows_by_symbol[row["symbol"]].append(row)
    labels: dict[tuple[str, str], float] = {}
    for symbol, rows in rows_by_symbol.items():
        rows = sorted(rows, key=lambda row: row["date"])
        for i, row in enumerate(rows):
            j = i + horizon
            if j >= len(rows):
                continue
            close = to_float(row["close"])
            future_close = to_float(rows[j]["close"])
            if close > 0:
                labels[(row["date"], symbol)] = future_close / close - 1
    return labels


def main() -> int:
    args = parse_args()
    labels = build_labels(Path(args.panel), args.horizon)
    by_factor_date: dict[str, dict[str, list[tuple[float, float]]]] = defaultdict(lambda: defaultdict(list))

    with Path(args.factors).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        factor_names = [name for name in (reader.fieldnames or []) if name not in {"date", "symbol", "ts_code"}]
        for row in reader:
            key = (row["date"], row["symbol"])
            if key not in labels:
                continue
            label = labels[key]
            for factor in factor_names:
                value = to_float(row[factor])
                if not math.isnan(value):
                    by_factor_date[factor][row["date"]].append((value, label))

    result_rows: list[dict[str, str]] = []
    for factor in sorted(by_factor_date):
        ic_values: list[float] = []
        rankic_values: list[float] = []
        n_total = 0
        for date in sorted(by_factor_date[factor]):
            pairs = by_factor_date[factor][date]
            if len(pairs) < 2:
                continue
            scores = [score for score, _ in pairs]
            day_labels = [label for _, label in pairs]
            ic_values.append(pearson_corr(scores, day_labels))
            rankic_values.append(spearman_corr(scores, day_labels))
            n_total += len(pairs)
        result_rows.append(
            {
                "factor": factor,
                "n": str(n_total),
                "dates": str(len(ic_values)),
                "ic": f"{safe_mean(ic_values):.8f}",
                "rankic": f"{safe_mean(rankic_values):.8f}",
                "icir": f"{safe_ir(ic_values):.8f}",
                "rankicir": f"{safe_ir(rankic_values):.8f}",
            }
        )

    result_rows.sort(key=lambda row: abs(float(row["rankic"])) if row["rankic"] != "nan" else -1, reverse=True)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["factor", "n", "dates", "ic", "rankic", "icir", "rankicir"])
        writer.writeheader()
        writer.writerows(result_rows)

    print(f"results={out_path} factors={len(result_rows)} labels={len(labels)}")
    for row in result_rows[:10]:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


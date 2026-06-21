"""Backtest externally generated scores with the local TopK trading protocol."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from run_trade_validation import (  # noqa: E402
    backtest,
    performance_stats,
    read_industry,
    read_meta,
    residualize_scores,
    write_daily,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", required=True, help="CSV with at least date,symbol,score columns.")
    parser.add_argument("--panel", required=True, help="Local panel CSV used to compute H5 labels and metadata.")
    parser.add_argument("--stock-basic", required=True, help="Tushare stock_basic CSV with industry metadata.")
    parser.add_argument("--method", required=True, help="Method name for output files and summary rows.")
    parser.add_argument("--date-column", default="date")
    parser.add_argument("--symbol-column", default="symbol")
    parser.add_argument("--score-column", default="score")
    parser.add_argument("--label-column", default="", help="Optional label column in the score CSV.")
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--topk", type=int, default=30)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2024-12-31")
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments" / "full_method_comparison"))
    return parser.parse_args()


def to_float(value: str | float | None) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def load_label_lookup(panel_path: Path, horizon: int) -> dict[tuple[str, str], float]:
    by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with panel_path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            by_symbol[row["symbol"]].append(row)

    labels: dict[tuple[str, str], float] = {}
    for symbol, rows in by_symbol.items():
        rows.sort(key=lambda row: row["date"])
        for idx in range(0, len(rows) - horizon):
            now = rows[idx]
            future = rows[idx + horizon]
            close = to_float(now.get("close"))
            future_close = to_float(future.get("close"))
            if close > 0 and math.isfinite(close) and math.isfinite(future_close):
                labels[(now["date"], symbol)] = future_close / close - 1.0
    return labels


def load_scored_rows(args: argparse.Namespace) -> list[dict]:
    panel_path = Path(args.panel)
    stock_basic_path = Path(args.stock_basic)
    meta = read_meta(panel_path, read_industry(stock_basic_path))
    label_lookup = load_label_lookup(panel_path, args.horizon)

    scored_rows: list[dict] = []
    with Path(args.scores).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = [args.date_column, args.symbol_column, args.score_column]
        missing = [field for field in required if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"score CSV missing required columns: {missing}")

        for row in reader:
            date = row[args.date_column]
            symbol = row[args.symbol_column]
            if not (args.test_start <= date <= args.test_end):
                continue
            score = to_float(row[args.score_column])
            if not math.isfinite(score):
                continue
            if args.label_column:
                label = to_float(row.get(args.label_column))
            else:
                label = label_lookup.get((date, symbol), float("nan"))
            if not math.isfinite(label):
                continue
            row_meta = meta.get((date, symbol), {})
            scored_rows.append(
                {
                    "date": date,
                    "symbol": symbol,
                    "score": score,
                    "label": label,
                    "industry": row_meta.get("industry", "UNKNOWN"),
                    "total_mv": float(row_meta.get("total_mv", float("nan"))),
                }
            )
    return scored_rows


def add_neutral_scores(scored_rows: list[dict]) -> None:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in scored_rows:
        by_date[row["date"]].append(row)
    for rows in by_date.values():
        residuals = residualize_scores(rows)
        for row, residual in zip(rows, residuals):
            row["neutral_score"] = float(residual)


def write_summary(path: Path, rows: list[dict]) -> None:
    fields = [
        "method",
        "variant",
        "horizon",
        "topk",
        "cost_bps",
        "days",
        "ann_return",
        "ann_vol",
        "sharpe",
        "mdd",
        "cum_return",
        "active_ann_return",
        "active_sharpe",
        "avg_turnover",
        "hit_rate",
        "avg_max_industry_weight",
        "avg_size_exposure",
        "yearly_ann_returns",
        "daily_source",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir

    scored_rows = load_scored_rows(args)
    if not scored_rows:
        raise RuntimeError("no scored rows after joining scores, labels, and test window")
    add_neutral_scores(scored_rows)

    summary_rows: list[dict] = []
    for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
        daily = backtest(scored_rows, score_field, args.topk, args.horizon, args.cost_bps)
        daily_path = out_dir / f"{args.method}_h{args.horizon}_top{args.topk}_{variant}_daily.csv"
        write_daily(daily_path, daily)
        stats = performance_stats(daily, "net_return")
        active_stats = performance_stats(daily, "net_active_return")
        years = sorted(set(row["date"][:4] for row in daily))
        yearly_returns = []
        for year in years:
            year_rows = [row for row in daily if row["date"].startswith(year)]
            yearly_returns.append((year, performance_stats(year_rows, "net_return")["ann_return"]))
        summary_rows.append(
            {
                "method": args.method,
                "variant": variant,
                "horizon": str(args.horizon),
                "topk": str(args.topk),
                "cost_bps": f"{args.cost_bps:.2f}",
                "days": str(len(daily)),
                "ann_return": f"{stats['ann_return']:.8f}",
                "ann_vol": f"{stats['ann_vol']:.8f}",
                "sharpe": f"{stats['sharpe']:.8f}",
                "mdd": f"{stats['mdd']:.8f}",
                "cum_return": f"{stats['cum_return']:.8f}",
                "active_ann_return": f"{active_stats['ann_return']:.8f}",
                "active_sharpe": f"{active_stats['sharpe']:.8f}",
                "avg_turnover": f"{stats['avg_turnover']:.8f}",
                "hit_rate": f"{stats['hit_rate']:.8f}",
                "avg_max_industry_weight": f"{float(np.mean([row['max_industry_weight'] for row in daily])):.8f}",
                "avg_size_exposure": f"{float(np.mean([row['size_exposure'] for row in daily])):.8f}",
                "yearly_ann_returns": ";".join(f"{year}:{value:.4f}" for year, value in yearly_returns),
                "daily_source": str(daily_path.relative_to(PROJECT_ROOT)),
            }
        )

    write_summary(out_dir / f"{args.method}_trade_validation_summary.csv", summary_rows)
    print(f"wrote {out_dir / f'{args.method}_trade_validation_summary.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


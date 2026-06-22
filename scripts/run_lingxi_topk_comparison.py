"""Compare Lingxi TopK variants with the two strongest runner-up proxies."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from run_trade_validation import (  # noqa: E402
    backtest,
    fit_predictions,
    performance_stats,
    read_industry,
    read_meta,
    residualize_scores,
    write_daily,
)
from run_unvalidated_paper_candidates import (  # noqa: E402
    add_meta,
    add_neutral_scores,
    build_examples,
    generate_scores,
    load_panel,
)


MARKETS = {
    "cn_a_share": {
        "panel": PROJECT_ROOT / "data/processed/cn_a_share/csi300_2018_2026_ytd/panel.csv",
        "stock_basic": PROJECT_ROOT / "data/raw/tushare/csi300_2025_2026/stock_basic.csv",
        "valid_start": "2022-01-04",
    },
    "us_large_cap": {
        "panel": PROJECT_ROOT / "data/processed/global_markets/us_large_cap_2018_2026/panel.csv",
        "stock_basic": PROJECT_ROOT / "data/processed/global_markets/us_large_cap_2018_2026/stock_basic.csv",
        "valid_start": "2022-01-03",
    },
    "hk_large_cap": {
        "panel": PROJECT_ROOT / "data/processed/global_markets/hk_large_cap_2018_2026/panel.csv",
        "stock_basic": PROJECT_ROOT / "data/processed/global_markets/hk_large_cap_2018_2026/stock_basic.csv",
        "valid_start": "2022-01-03",
    },
}

RUNNER_METHODS = {
    "qlib_alpha158": "2020_qlib_yang",
    "fintsb_ts": "2025_fintsb",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--market", action="append", choices=sorted(MARKETS))
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--lookback", type=int, default=20)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--valid-end", default="2022-12-30")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2025-12-31")
    parser.add_argument("--ridge-alpha", type=float, default=10.0)
    parser.add_argument("--candidate-ridge-alpha", type=float, default=25.0)
    parser.add_argument("--max-train-rows", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_topk_comparison"))
    return parser.parse_args()


def add_lingxi_neutral_scores(scored_rows: list[dict]) -> None:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in scored_rows:
        by_date[row["date"]].append(row)
    for rows in by_date.values():
        residuals = residualize_scores(rows)
        for row, residual in zip(rows, residuals):
            row["neutral_score"] = float(residual)


def build_lingxi_scores(args: argparse.Namespace, market: str, panel: Path, stock_basic: Path) -> list[dict]:
    local_args = argparse.Namespace(**vars(args))
    local_args.panel = str(panel)
    local_args.stock_basic = str(stock_basic)
    local_args.model = ["rd_agent_quant"]
    rows, preds = fit_predictions(local_args, "rd_agent_quant")
    meta = read_meta(panel, read_industry(stock_basic))
    scored_rows = []
    for row, score in zip(rows, preds):
        row_meta = meta.get((row["date"], row["symbol"]), {})
        scored_rows.append(
            {
                "date": row["date"],
                "symbol": row["symbol"],
                "score": float(score),
                "label": float(row["label"]),
                "industry": row_meta.get("industry", "UNKNOWN"),
                "total_mv": float(row_meta.get("total_mv", float("nan"))),
            }
        )
    add_lingxi_neutral_scores(scored_rows)
    print(f"{market} lingxi scored_rows={len(scored_rows)}")
    return scored_rows


def build_runner_scores(args: argparse.Namespace, market: str, panel: Path, stock_basic: Path) -> dict[str, list[dict]]:
    candidate_args = argparse.Namespace(**vars(args))
    candidate_args.panel = str(panel)
    candidate_args.stock_basic = str(stock_basic)
    candidate_args.market = market
    candidate_args.valid_start = MARKETS[market]["valid_start"]
    candidate_args.ridge_alpha = args.candidate_ridge_alpha
    rows = build_examples(load_panel(panel), args.horizon)
    outputs: dict[str, list[dict]] = {}
    for label, paper_id in RUNNER_METHODS.items():
        scored, _ = generate_scores(candidate_args, paper_id, rows)
        add_meta(scored, panel, stock_basic)
        add_neutral_scores(scored)
        outputs[label] = scored
        print(f"{market} {label} scored_rows={len(scored)}")
    return outputs


def summarize_daily(
    out_dir: Path,
    market: str,
    method: str,
    topk: int,
    variant: str,
    score_field: str,
    scored_rows: list[dict],
    args: argparse.Namespace,
) -> dict[str, str]:
    daily = backtest(scored_rows, score_field, topk, args.horizon, args.cost_bps)
    daily_path = out_dir / market / f"{method}_h{args.horizon}_top{topk}_{variant}_daily.csv"
    write_daily(daily_path, daily)
    stats = performance_stats(daily, "net_return")
    active_stats = performance_stats(daily, "net_active_return")
    years = sorted(set(row["date"][:4] for row in daily))
    yearly_returns = []
    for year in years:
        year_rows = [row for row in daily if row["date"].startswith(year)]
        yearly_returns.append((year, performance_stats(year_rows, "net_return")["ann_return"]))
    return {
        "market": market,
        "method": method,
        "variant": variant,
        "horizon": str(args.horizon),
        "topk": str(topk),
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


def write_summary(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "market",
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
    markets = args.market or ["cn_a_share", "us_large_cap", "hk_large_cap"]
    topks = sorted(set(args.topk or [5, 10, 20, 30]), reverse=True)
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir

    summary_rows: list[dict[str, str]] = []
    for market in markets:
        config = MARKETS[market]
        args.valid_start = config["valid_start"]
        panel = config["panel"]
        stock_basic = config["stock_basic"]
        method_scores = {"lingxi": build_lingxi_scores(args, market, panel, stock_basic)}
        method_scores.update(build_runner_scores(args, market, panel, stock_basic))
        for method, scored_rows in method_scores.items():
            for topk in topks:
                for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
                    row = summarize_daily(out_dir, market, method, topk, variant, score_field, scored_rows, args)
                    summary_rows.append(row)
                    print(market, method, f"top{topk}", variant, row["ann_return"], row["sharpe"], row["mdd"])

    write_summary(out_dir / "lingxi_topk_comparison_summary.csv", summary_rows)
    print(f"summary={out_dir / 'lingxi_topk_comparison_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

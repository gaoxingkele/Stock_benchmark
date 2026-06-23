"""Validate a conservative CASE-Lingxi context router.

This router is deliberately constrained. It does not learn arbitrary daily
stock weights and it does not select from unapproved research sleeves. It only
routes between already validated Lingxi-family sleeves, using lagged market
stress and lagged sleeve evidence.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import run_lingxi_adaptive_router_validation as base  # noqa: E402
import run_lingxi_regime_router_validation as regime_base  # noqa: E402


ROUTER_NAME = "case_lingxi_context_router"
MENU_NAME = "case_lingxi_static_menu"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=str(PROJECT_ROOT / "experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/case_lingxi_context_router_validation_2026_ytd"))
    parser.add_argument("--market", action="append", choices=base.MARKETS)
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--variant", action="append", choices=base.VARIANTS)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--min-history", type=int, default=30)
    parser.add_argument("--risk-drawdown", type=float, default=-0.05)
    parser.add_argument("--vol-lookback", type=int, default=120)
    parser.add_argument("--vol-quantile", type=float, default=0.75)
    parser.add_argument("--switch-margin", type=float, default=0.00015)
    parser.add_argument("--risk-aversion", type=float, default=0.35)
    parser.add_argument("--drawdown-penalty", type=float, default=0.10)
    parser.add_argument("--turnover-penalty", type=float, default=0.15)
    parser.add_argument("--switch-penalty", type=float, default=0.00025)
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def production_menu_method(market: str, topk: int, variant: str) -> str:
    """Return the conservative fixed sleeve from the current benchmark table."""
    if market == "hk_large_cap":
        return "lingxi_pitnorm"
    if market == "crypto_major" and variant == "raw":
        return "lingxi_pitnorm_gate_return_floor"
    if market == "us_large_cap" and topk == 10:
        return "lingxi_pitnorm"
    return "lingxi"


def risk_sleeves(market: str, variant: str) -> list[str]:
    if market == "crypto_major" and variant == "raw":
        return ["lingxi_pitnorm_gate_return_floor", "lingxi_pitnorm", "lingxi"]
    return ["lingxi_pitnorm", "lingxi_pitnorm_gate_return_floor", "lingxi"]


def trailing_values(regime: dict[str, dict[str, float]], dates: list[str], idx: int, field: str, lookback: int, horizon: int) -> list[float]:
    end = idx - horizon
    if end <= 0:
        return []
    start = max(0, end - lookback)
    return [float(regime.get(dates[item], {}).get(field, 0.0)) for item in range(start, end)]


def is_market_stressed(regime: dict[str, dict[str, float]], dates: list[str], idx: int, args: argparse.Namespace) -> bool:
    end = idx - args.horizon
    if end <= 0:
        return False
    row = regime.get(dates[end], {})
    drawdown = float(row.get("drawdown60", 0.0))
    vol = float(row.get("vol20", 0.0))
    vol_hist = trailing_values(regime, dates, idx, "vol20", args.vol_lookback, args.horizon)
    vol_gate = float(np.quantile(vol_hist, args.vol_quantile)) if len(vol_hist) >= args.min_history else float("inf")
    weak_breadth = float(row.get("breadth20", 0.5)) < 0.45
    return drawdown <= args.risk_drawdown or vol >= vol_gate or (drawdown < -0.025 and weak_breadth)


def lagged_score(series: dict[str, list[dict]], method: str, idx: int, args: argparse.Namespace) -> float:
    end = idx - args.horizon
    if end < args.min_history:
        return -1e9
    start = max(0, end - args.window)
    returns = [float(series[method][item]["net_return"]) for item in range(start, end)]
    turnovers = [float(series[method][item]["turnover"]) for item in range(start, end)]
    if not returns:
        return -1e9
    return base.rolling_metric(returns, turnovers, args)


def make_fixed_method_rows(dates: list[str], series: dict[str, list[dict]], method: str) -> list[dict]:
    rows = []
    for idx, date in enumerate(dates):
        weights = {name: 1.0 if name == method else 0.0 for name in base.METHODS}
        method_returns = {name: series[name][idx] for name in base.METHODS}
        rows.append(base.combine_row(date, method_returns, weights, method, False))
    return rows


def make_static_menu_rows(dates: list[str], series: dict[str, list[dict]], market: str, topk: int, variant: str) -> list[dict]:
    return make_fixed_method_rows(dates, series, production_menu_method(market, topk, variant))


def make_context_router_rows(
    dates: list[str],
    series: dict[str, list[dict]],
    regime: dict[str, dict[str, float]],
    market: str,
    topk: int,
    variant: str,
    args: argparse.Namespace,
) -> list[dict]:
    rows = []
    previous = None
    default_method = production_menu_method(market, topk, variant)
    sleeves = risk_sleeves(market, variant)
    for idx, date in enumerate(dates):
        selected = default_method
        if is_market_stressed(regime, dates, idx, args):
            default_score = lagged_score(series, default_method, idx, args)
            scores = {method: lagged_score(series, method, idx, args) for method in sleeves}
            best_risk = max(scores, key=scores.get)
            if scores[best_risk] >= default_score - args.switch_margin:
                selected = best_risk
        if previous and previous != selected:
            selected_score = lagged_score(series, selected, idx, args) - args.switch_penalty
            previous_score = lagged_score(series, previous, idx, args)
            if previous_score >= selected_score:
                selected = previous
        weights = {method: 1.0 if method == selected else 0.0 for method in base.METHODS}
        method_returns = {method: series[method][idx] for method in base.METHODS}
        rows.append(base.combine_row(date, method_returns, weights, selected, previous is not None and previous != selected))
        previous = selected
    return rows


def write_summary(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    source_dir = resolve(args.source_dir)
    out_dir = resolve(args.out_dir)
    markets = args.market or base.MARKETS
    topks = sorted(set(args.topk or [10, 5]), reverse=True)
    variants = args.variant or base.VARIANTS
    labels = {
        **base.METHOD_LABELS,
        MENU_NAME: "CASE-Lingxi static production menu",
        ROUTER_NAME: "CASE-Lingxi conservative context router",
    }
    summary_rows: list[dict[str, str]] = []

    for market in markets:
        regime = regime_base.read_panel_daily_features(regime_base.PANEL_PATHS[market])
        for topk in topks:
            for variant in variants:
                dates, series = base.align_methods(source_dir, market, topk, variant)
                outputs = {
                    MENU_NAME: make_static_menu_rows(dates, series, market, topk, variant),
                    ROUTER_NAME: make_context_router_rows(dates, series, regime, market, topk, variant, args),
                    "static_equal_ensemble": base.make_static_ensemble(dates, series),
                    "oracle_upper_bound": base.make_oracle(dates, series),
                }
                for method in base.METHODS:
                    outputs[method] = make_fixed_method_rows(dates, series, method)

                for method, rows in outputs.items():
                    daily_path = out_dir / market / f"{method}_h5_top{topk}_{variant}_daily.csv"
                    base.write_router_daily(daily_path, rows)
                    summary = base.summarize(method, market, topk, variant, rows, daily_path)
                    summary["method_label"] = labels.get(method, method)
                    summary_rows.append(summary)
                    print(market, f"top{topk}", variant, method, summary["ann_return"], summary["sharpe"], summary["mdd"])

    write_summary(out_dir / "case_lingxi_context_router_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'case_lingxi_context_router_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

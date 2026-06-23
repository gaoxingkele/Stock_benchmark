"""Research-only RL-style router baseline for CASE-Lingxi.

The policy is intentionally small and frozen before OOS evaluation. It uses
full-information sleeve returns in the training period to learn a tabular
state-action value table, then routes only among approved Lingxi-family sleeves.
It is a research baseline, not a production strategy.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import run_case_lingxi_context_router as context_base  # noqa: E402
import run_lingxi_adaptive_router_validation as base  # noqa: E402
import run_lingxi_regime_router_validation as regime_base  # noqa: E402


RL_NAME = "case_lingxi_tabular_rl_router"
MENU_NAME = context_base.MENU_NAME
CONTEXT_NAME = context_base.ROUTER_NAME


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=str(PROJECT_ROOT / "experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/case_lingxi_rl_router_validation_2025_2026_ytd"))
    parser.add_argument("--market", action="append", choices=base.MARKETS)
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--variant", action="append", choices=base.VARIANTS)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--train-end", default="2024-12-31")
    parser.add_argument("--test-start", default="2025-01-01")
    parser.add_argument("--gamma", type=float, default=0.20)
    parser.add_argument("--risk-aversion", type=float, default=0.35)
    parser.add_argument("--drawdown-penalty", type=float, default=0.10)
    parser.add_argument("--turnover-penalty", type=float, default=0.15)
    parser.add_argument("--switch-penalty", type=float, default=0.00025)
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--min-history", type=int, default=30)
    parser.add_argument("--risk-drawdown", type=float, default=-0.05)
    parser.add_argument("--vol-lookback", type=int, default=120)
    parser.add_argument("--vol-quantile", type=float, default=0.75)
    parser.add_argument("--switch-margin", type=float, default=0.00015)
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def train_thresholds(regime: dict[str, dict[str, float]], dates: list[str], train_end: str) -> dict[str, float]:
    train_dates = [date for date in dates if date <= train_end and date in regime]
    fields = {
        "vol20": [float(regime[date].get("vol20", 0.0)) for date in train_dates],
        "dispersion20": [float(regime[date].get("dispersion20", 0.0)) for date in train_dates],
        "breadth20": [float(regime[date].get("breadth20", 0.5)) for date in train_dates],
    }
    return {
        "vol20_med": float(np.median(fields["vol20"])) if fields["vol20"] else 0.0,
        "dispersion20_med": float(np.median(fields["dispersion20"])) if fields["dispersion20"] else 0.0,
        "breadth20_med": float(np.median(fields["breadth20"])) if fields["breadth20"] else 0.5,
    }


def state_key(regime: dict[str, dict[str, float]], dates: list[str], idx: int, thresholds: dict[str, float], args: argparse.Namespace) -> tuple[int, int, int, int, int]:
    end = idx - args.horizon
    if end <= 0:
        return (0, 0, 0, 0, 0)
    row = regime.get(dates[end], {})
    trend = 1 if float(row.get("mom20", 0.0)) > 0 else 0
    high_vol = 1 if float(row.get("vol20", 0.0)) > thresholds["vol20_med"] else 0
    drawdown = 1 if float(row.get("drawdown60", 0.0)) < args.risk_drawdown else 0
    weak_breadth = 1 if float(row.get("breadth20", 0.5)) < thresholds["breadth20_med"] else 0
    high_dispersion = 1 if float(row.get("dispersion20", 0.0)) > thresholds["dispersion20_med"] else 0
    return (trend, high_vol, drawdown, weak_breadth, high_dispersion)


def reward(series: dict[str, list[dict]], method: str, idx: int, previous: str | None, args: argparse.Namespace) -> float:
    row = series[method][idx]
    switch_cost = args.switch_penalty if previous and previous != method else 0.0
    return float(row["net_return"]) - args.turnover_penalty * float(row["turnover"]) * 0.001 - switch_cost


def fit_q_table(
    dates: list[str],
    series: dict[str, list[dict]],
    regime: dict[str, dict[str, float]],
    thresholds: dict[str, float],
    args: argparse.Namespace,
) -> dict[tuple[int, int, int, int, int], dict[str, float]]:
    sums: dict[tuple[int, int, int, int, int], dict[str, float]] = defaultdict(lambda: {method: 0.0 for method in base.METHODS})
    counts: dict[tuple[int, int, int, int, int], dict[str, int]] = defaultdict(lambda: {method: 0 for method in base.METHODS})

    train_indices = [idx for idx, date in enumerate(dates) if date <= args.train_end and idx >= args.horizon]
    for idx in reversed(train_indices):
        state = state_key(regime, dates, idx, thresholds, args)
        next_state = state_key(regime, dates, min(idx + 1, len(dates) - 1), thresholds, args)
        next_best = max(
            (sums[next_state][method] / counts[next_state][method]) if counts[next_state][method] else 0.0
            for method in base.METHODS
        )
        for method in base.METHODS:
            value = reward(series, method, idx, None, args) + args.gamma * next_best
            sums[state][method] += value
            counts[state][method] += 1

    q_table: dict[tuple[int, int, int, int, int], dict[str, float]] = {}
    for state, method_sums in sums.items():
        q_table[state] = {}
        for method in base.METHODS:
            q_table[state][method] = method_sums[method] / counts[state][method] if counts[state][method] else -1e9
    return q_table


def make_rl_rows(
    dates: list[str],
    series: dict[str, list[dict]],
    regime: dict[str, dict[str, float]],
    market: str,
    topk: int,
    variant: str,
    args: argparse.Namespace,
) -> list[dict]:
    thresholds = train_thresholds(regime, dates, args.train_end)
    q_table = fit_q_table(dates, series, regime, thresholds, args)
    previous = None
    rows = []
    default_method = context_base.production_menu_method(market, topk, variant)
    for idx, date in enumerate(dates):
        if date < args.test_start:
            previous = None
            continue
        state = state_key(regime, dates, idx, thresholds, args)
        q_values = q_table.get(state)
        selected = default_method
        if q_values:
            selected = max(base.METHODS, key=lambda method: q_values.get(method, -1e9))
        if previous and previous != selected:
            selected_score = q_values.get(selected, -1e9) - args.switch_penalty if q_values else -1e9
            previous_score = q_values.get(previous, -1e9) if q_values else -1e9
            if previous_score >= selected_score:
                selected = previous
        weights = {method: 1.0 if method == selected else 0.0 for method in base.METHODS}
        method_returns = {method: series[method][idx] for method in base.METHODS}
        rows.append(base.combine_row(date, method_returns, weights, selected, previous is not None and previous != selected))
        previous = selected
    return rows


def oos_rows(rows: list[dict], test_start: str) -> list[dict]:
    return [row for row in rows if row["date"] >= test_start]


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
        CONTEXT_NAME: "CASE-Lingxi conservative context router",
        RL_NAME: "CASE-Lingxi frozen tabular RL router",
    }
    summary_rows: list[dict[str, str]] = []

    for market in markets:
        regime = regime_base.read_panel_daily_features(regime_base.PANEL_PATHS[market])
        for topk in topks:
            for variant in variants:
                dates, series = base.align_methods(source_dir, market, topk, variant)
                outputs = {
                    MENU_NAME: oos_rows(context_base.make_static_menu_rows(dates, series, market, topk, variant), args.test_start),
                    CONTEXT_NAME: oos_rows(context_base.make_context_router_rows(dates, series, regime, market, topk, variant, args), args.test_start),
                    RL_NAME: make_rl_rows(dates, series, regime, market, topk, variant, args),
                    "static_equal_ensemble": oos_rows(base.make_static_ensemble(dates, series), args.test_start),
                    "oracle_upper_bound": oos_rows(base.make_oracle(dates, series), args.test_start),
                }
                for method in base.METHODS:
                    outputs[method] = oos_rows(context_base.make_fixed_method_rows(dates, series, method), args.test_start)

                for method, rows in outputs.items():
                    daily_path = out_dir / market / f"{method}_h5_top{topk}_{variant}_daily.csv"
                    base.write_router_daily(daily_path, rows)
                    summary = base.summarize(method, market, topk, variant, rows, daily_path)
                    summary["method_label"] = labels.get(method, method)
                    summary["train_end"] = args.train_end
                    summary["test_start"] = args.test_start
                    summary_rows.append(summary)
                    print(market, f"top{topk}", variant, method, summary["ann_return"], summary["sharpe"], summary["mdd"])

    write_summary(out_dir / "case_lingxi_rl_router_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'case_lingxi_rl_router_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

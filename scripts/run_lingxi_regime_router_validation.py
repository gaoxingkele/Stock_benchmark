"""Validate a market-regime enhanced Lingxi adaptive router.

This is the second-stage router experiment. It keeps the same tradable sleeves
as the first adaptive router, but adds lagged market-regime features derived
from the underlying panel: market trend, volatility, drawdown, breadth,
dispersion, liquidity, and size concentration.
"""

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

import run_lingxi_adaptive_router_validation as base  # noqa: E402


PANEL_PATHS = {
    "cn_a_share": PROJECT_ROOT / "data/processed/cn_a_share/csi300_2018_2026_ytd/panel.csv",
    "us_large_cap": PROJECT_ROOT / "data/processed/global_markets/us_large_cap_2018_2026/panel.csv",
    "hk_large_cap": PROJECT_ROOT / "data/processed/global_markets/hk_large_cap_2018_2026/panel.csv",
    "crypto_major": PROJECT_ROOT / "data/processed/global_markets/crypto_major_2018_2026/panel.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=str(PROJECT_ROOT / "experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_regime_router_validation_2026_ytd"))
    parser.add_argument("--market", action="append", choices=base.MARKETS)
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--variant", action="append", choices=base.VARIANTS)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--min-history", type=int, default=30)
    parser.add_argument("--ridge-alpha", type=float, default=4.0)
    parser.add_argument("--ridge-refit-step", type=int, default=5)
    parser.add_argument("--turnover-penalty", type=float, default=0.15)
    parser.add_argument("--switch-penalty", type=float, default=0.00025)
    return parser.parse_args()


def safe_float(value: str | None, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
        return out if math.isfinite(out) else default
    except ValueError:
        return default


def read_panel_daily_features(path: Path) -> dict[str, dict[str, float]]:
    by_symbol: dict[str, list[dict]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            by_symbol[row["symbol"]].append(row)

    by_date: dict[str, list[dict[str, float]]] = defaultdict(list)
    for symbol_rows in by_symbol.values():
        symbol_rows.sort(key=lambda row: row["date"])
        previous_close = None
        for row in symbol_rows:
            close = safe_float(row.get("close"), float("nan"))
            pre_close = safe_float(row.get("pre_close"), previous_close if previous_close is not None else close)
            if previous_close is not None and previous_close > 0:
                ret = close / previous_close - 1.0
            elif pre_close and pre_close > 0:
                ret = close / pre_close - 1.0
            else:
                ret = safe_float(row.get("pct_chg")) / 100.0
            amount = safe_float(row.get("amount"))
            total_mv = safe_float(row.get("total_mv"))
            by_date[row["date"]].append({"ret": ret, "amount": amount, "total_mv": total_mv})
            previous_close = close if close > 0 else previous_close

    raw: dict[str, dict[str, float]] = {}
    nav = 1.0
    navs: list[float] = []
    dates = sorted(by_date)
    for date in dates:
        rows = by_date[date]
        returns = np.asarray([row["ret"] for row in rows], dtype=float)
        finite = np.isfinite(returns)
        returns = returns[finite]
        if returns.size == 0:
            equal_ret = 0.0
            dispersion = 0.0
            breadth = 0.5
            tail_spread = 0.0
        else:
            equal_ret = float(np.mean(returns))
            dispersion = float(np.std(returns))
            breadth = float(np.mean(returns > 0.0))
            tail_spread = float(np.percentile(returns, 80) - np.percentile(returns, 20))

        amount = float(np.nansum([row["amount"] for row in rows]))
        mv_values = np.asarray([row["total_mv"] for row in rows if row["total_mv"] > 0], dtype=float)
        if mv_values.size:
            mv_sum = float(np.sum(mv_values))
            hhi = float(np.sum((mv_values / mv_sum) ** 2))
            top20_share = float(np.sum(np.sort(mv_values)[-max(1, int(len(mv_values) * 0.2)) :]) / mv_sum)
        else:
            hhi = 0.0
            top20_share = 0.0
        nav *= 1.0 + equal_ret
        navs.append(nav)
        raw[date] = {
            "equal_ret": equal_ret,
            "dispersion": dispersion,
            "breadth": breadth,
            "tail_spread": tail_spread,
            "amount": amount,
            "size_hhi": hhi,
            "top20_size_share": top20_share,
            "nav": nav,
        }

    features: dict[str, dict[str, float]] = {}
    for idx, date in enumerate(dates):
        start20 = max(0, idx - 19)
        start60 = max(0, idx - 59)
        window20 = dates[start20 : idx + 1]
        window60 = dates[start60 : idx + 1]
        ret20 = [raw[item]["equal_ret"] for item in window20]
        ret60 = [raw[item]["equal_ret"] for item in window60]
        amount20 = [raw[item]["amount"] for item in window20]
        nav60 = [raw[item]["nav"] for item in window60]
        peak60 = max(nav60) if nav60 else raw[date]["nav"]
        features[date] = {
            **raw[date],
            "mom20": float(np.prod([1.0 + value for value in ret20]) - 1.0),
            "mom60": float(np.prod([1.0 + value for value in ret60]) - 1.0),
            "vol20": float(np.std(ret20)) if len(ret20) > 1 else 0.0,
            "vol60": float(np.std(ret60)) if len(ret60) > 1 else 0.0,
            "drawdown60": raw[date]["nav"] / peak60 - 1.0 if peak60 > 0 else 0.0,
            "breadth20": float(np.mean([raw[item]["breadth"] for item in window20])),
            "dispersion20": float(np.mean([raw[item]["dispersion"] for item in window20])),
            "tail_spread20": float(np.mean([raw[item]["tail_spread"] for item in window20])),
            "amount20_change": (amount20[-1] / float(np.mean(amount20[:-1])) - 1.0) if len(amount20) > 1 and float(np.mean(amount20[:-1])) > 0 else 0.0,
        }
    return features


def lagged_regime_features(regime: dict[str, dict[str, float]], dates: list[str], idx: int, args: argparse.Namespace) -> list[float]:
    end = idx - args.horizon
    if end <= 0:
        return [0.0] * 13
    date = dates[end]
    row = regime.get(date, {})
    return [
        float(row.get("equal_ret", 0.0)),
        float(row.get("mom20", 0.0)),
        float(row.get("mom60", 0.0)),
        float(row.get("vol20", 0.0)),
        float(row.get("vol60", 0.0)),
        float(row.get("drawdown60", 0.0)),
        float(row.get("breadth", 0.5)),
        float(row.get("breadth20", 0.5)),
        float(row.get("dispersion20", 0.0)),
        float(row.get("tail_spread20", 0.0)),
        float(row.get("amount20_change", 0.0)),
        float(row.get("size_hhi", 0.0)),
        float(row.get("top20_size_share", 0.0)),
    ]


def context_features(
    series: dict[str, list[dict]],
    regime: dict[str, dict[str, float]],
    dates: list[str],
    idx: int,
    method: str,
    args: argparse.Namespace,
) -> list[float]:
    return [*base.context_features(series, idx, method, args), *lagged_regime_features(regime, dates, idx, args)]


def make_regime_ridge_router(
    dates: list[str],
    series: dict[str, list[dict]],
    regime: dict[str, dict[str, float]],
    args: argparse.Namespace,
) -> list[dict]:
    rows = []
    previous = None
    cached_selected = "lingxi"
    for idx, date in enumerate(dates):
        selected = cached_selected
        train_end = idx - args.horizon
        should_refit = idx < args.min_history + args.horizon or idx % max(1, args.ridge_refit_step) == 0
        if should_refit and train_end >= args.min_history:
            train_start = max(args.horizon, train_end - args.window * 3)
            predictions = {}
            for method in base.METHODS:
                xs = [context_features(series, regime, dates, j, method, args) for j in range(train_start, train_end)]
                ys = [base.reward_at(series, j, method, None, args) for j in range(train_start, train_end)]
                if len(xs) >= args.min_history:
                    try:
                        coef = base.fit_ridge(xs, ys, args.ridge_alpha)
                        pred = float(np.dot(context_features(series, regime, dates, idx, method, args), coef))
                    except np.linalg.LinAlgError:
                        pred = float(np.mean(ys))
                    if previous and previous != method:
                        pred -= args.switch_penalty
                    predictions[method] = pred
            if predictions:
                selected = max(predictions, key=predictions.get)
                cached_selected = selected
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
    source_dir = base.resolve(args.source_dir)
    out_dir = base.resolve(args.out_dir)
    markets = args.market or base.MARKETS
    topks = sorted(set(args.topk or [10, 5]), reverse=True)
    variants = args.variant or base.VARIANTS
    summary_rows: list[dict[str, str]] = []
    labels = {**base.METHOD_LABELS, "market_regime_ridge_router": "Market-regime ridge router"}

    for market in markets:
        regime = read_panel_daily_features(PANEL_PATHS[market])
        for topk in topks:
            for variant in variants:
                dates, series = base.align_methods(source_dir, market, topk, variant)
                outputs = {
                    "static_equal_ensemble": base.make_static_ensemble(dates, series),
                    "contextual_ridge_router": base.make_contextual_ridge_router(dates, series, args),
                    "market_regime_ridge_router": make_regime_ridge_router(dates, series, regime, args),
                    "oracle_upper_bound": base.make_oracle(dates, series),
                }
                for method in base.METHODS:
                    outputs[method] = []
                    for idx, date in enumerate(dates):
                        weights = {name: 1.0 if name == method else 0.0 for name in base.METHODS}
                        method_returns = {name: series[name][idx] for name in base.METHODS}
                        outputs[method].append(base.combine_row(date, method_returns, weights, method, False))

                for method, rows in outputs.items():
                    daily_path = out_dir / market / f"{method}_h5_top{topk}_{variant}_daily.csv"
                    base.write_router_daily(daily_path, rows)
                    summary = base.summarize(method, market, topk, variant, rows, daily_path)
                    summary["method_label"] = labels.get(method, method)
                    summary_rows.append(summary)
                    print(market, f"top{topk}", variant, method, summary["ann_return"], summary["sharpe"], summary["mdd"])

    write_summary(out_dir / "lingxi_regime_router_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'lingxi_regime_router_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Validate dynamic strategy routers for the Lingxi adaptive suite.

This script works at the strategy daily-return layer. It reuses the already
validated Lingxi, PITNorm, and ReturnFloor-Gate daily files, then tests whether
lagged market/strategy context can route between them without lookahead.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from run_trade_validation import performance_stats  # noqa: E402


METHODS = ["lingxi", "lingxi_pitnorm", "lingxi_pitnorm_gate_return_floor"]
METHOD_LABELS = {
    "lingxi": "Lingxi",
    "lingxi_pitnorm": "PITNorm",
    "lingxi_pitnorm_gate_return_floor": "ReturnFloor-Gate",
    "static_equal_ensemble": "Static equal ensemble",
    "rolling_selector": "Rolling selector",
    "hedge_router": "Hedge router",
    "contextual_ridge_router": "Contextual ridge router",
    "oracle_upper_bound": "Oracle upper bound",
}
MARKETS = ["cn_a_share", "us_large_cap", "hk_large_cap", "crypto_major"]
VARIANTS = ["raw", "industry_size_neutral"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=str(PROJECT_ROOT / "experiments/lingxi_pitnorm_tuned_gate_validation"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_adaptive_router_validation"))
    parser.add_argument("--market", action="append", choices=MARKETS)
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--variant", action="append", choices=VARIANTS)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--min-history", type=int, default=30)
    parser.add_argument("--ridge-alpha", type=float, default=2.5)
    parser.add_argument("--ridge-refit-step", type=int, default=5)
    parser.add_argument("--hedge-eta", type=float, default=18.0)
    parser.add_argument("--risk-aversion", type=float, default=0.35)
    parser.add_argument("--drawdown-penalty", type=float, default=0.10)
    parser.add_argument("--turnover-penalty", type=float, default=0.15)
    parser.add_argument("--switch-penalty", type=float, default=0.00025)
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def read_daily(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    out = []
    for row in rows:
        out.append(
            {
                "date": row["date"],
                "net_return": float(row["net_return"]),
                "benchmark_return": float(row.get("benchmark_return", 0.0)),
                "net_active_return": float(row.get("net_active_return", 0.0)),
                "turnover": float(row.get("turnover", 0.0)),
                "cost": float(row.get("cost", 0.0)),
                "max_industry_weight": float(row.get("max_industry_weight", 0.0)),
                "size_exposure": float(row.get("size_exposure", 0.0)),
            }
        )
    return out


def max_drawdown(values: list[float]) -> float:
    nav = 1.0
    peak = 1.0
    worst = 0.0
    for value in values:
        nav *= 1.0 + value
        peak = max(peak, nav)
        worst = min(worst, nav / peak - 1.0)
    return worst


def ann_sharpe(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    vol = float(np.std(values))
    if vol <= 1e-12 or not math.isfinite(vol):
        return 0.0
    return float(np.mean(values) / vol * math.sqrt(252.0))


def rolling_metric(values: list[float], turnovers: list[float], args: argparse.Namespace) -> float:
    if not values:
        return 0.0
    mean = float(np.mean(values))
    vol = float(np.std(values))
    drawdown = abs(max_drawdown(values))
    turnover = float(np.mean(turnovers)) if turnovers else 0.0
    return mean - args.risk_aversion * vol - args.drawdown_penalty * drawdown / len(values) - args.turnover_penalty * turnover * 0.001


def align_methods(source_dir: Path, market: str, topk: int, variant: str) -> tuple[list[str], dict[str, list[dict]]]:
    aligned: dict[str, list[dict]] = {}
    date_sets = []
    for method in METHODS:
        path = source_dir / market / f"{method}_h5_top{topk}_{variant}_daily.csv"
        rows = read_daily(path)
        aligned[method] = rows
        date_sets.append({row["date"] for row in rows})
    dates = sorted(set.intersection(*date_sets))
    by_method = {method: {row["date"]: row for row in rows} for method, rows in aligned.items()}
    return dates, {method: [by_method[method][date] for date in dates] for method in METHODS}


def combine_row(date: str, method_returns: dict[str, dict], weights: dict[str, float], selected: str, switch: bool) -> dict:
    net_return = sum(weights[method] * method_returns[method]["net_return"] for method in METHODS)
    benchmark = method_returns["lingxi"]["benchmark_return"]
    turnover = sum(weights[method] * method_returns[method]["turnover"] for method in METHODS)
    max_industry = sum(weights[method] * method_returns[method]["max_industry_weight"] for method in METHODS)
    size = sum(weights[method] * method_returns[method]["size_exposure"] for method in METHODS)
    return {
        "date": date,
        "selected_method": selected,
        "net_return": net_return,
        "benchmark_return": benchmark,
        "net_active_return": net_return - benchmark,
        "turnover": turnover,
        "cost": sum(weights[method] * method_returns[method]["cost"] for method in METHODS),
        "max_industry_weight": max_industry,
        "size_exposure": size,
        "switch": 1.0 if switch else 0.0,
        **{f"weight_{method}": weights[method] for method in METHODS},
    }


def history_slice(series: dict[str, list[dict]], method: str, start: int, end: int, field: str) -> list[float]:
    return [float(row[field]) for row in series[method][start:end]]


def market_features(series: dict[str, list[dict]], idx: int, args: argparse.Namespace) -> list[float]:
    end = idx - args.horizon
    if end <= 0:
        return [0.0] * 8
    start20 = max(0, end - 20)
    start60 = max(0, end - 60)
    bench20 = [series["lingxi"][i]["benchmark_return"] for i in range(start20, end)]
    bench60 = [series["lingxi"][i]["benchmark_return"] for i in range(start60, end)]
    lingxi20 = [series["lingxi"][i]["net_return"] for i in range(start20, end)]
    pit20 = [series["lingxi_pitnorm"][i]["net_return"] for i in range(start20, end)]
    rf20 = [series["lingxi_pitnorm_gate_return_floor"][i]["net_return"] for i in range(start20, end)]
    return [
        float(np.mean(bench20)) if bench20 else 0.0,
        float(np.std(bench20)) if len(bench20) > 1 else 0.0,
        max_drawdown(bench60) if bench60 else 0.0,
        ann_sharpe(bench20),
        float(np.mean(lingxi20)) if lingxi20 else 0.0,
        float(np.mean(pit20)) if pit20 else 0.0,
        float(np.mean(rf20)) if rf20 else 0.0,
        float(np.mean(rf20) - np.mean(lingxi20)) if rf20 and lingxi20 else 0.0,
    ]


def context_features(series: dict[str, list[dict]], idx: int, method: str, args: argparse.Namespace) -> list[float]:
    end = idx - args.horizon
    if end <= 0:
        return [1.0, *([0.0] * 18)]
    start20 = max(0, end - 20)
    start40 = max(0, end - 40)
    rets20 = history_slice(series, method, start20, end, "net_return")
    rets40 = history_slice(series, method, start40, end, "net_return")
    turns20 = history_slice(series, method, start20, end, "turnover")
    ind20 = history_slice(series, method, start20, end, "max_industry_weight")
    size20 = history_slice(series, method, start20, end, "size_exposure")
    return [
        1.0,
        *market_features(series, idx, args),
        float(np.mean(rets20)) if rets20 else 0.0,
        float(np.std(rets20)) if len(rets20) > 1 else 0.0,
        max_drawdown(rets40) if rets40 else 0.0,
        ann_sharpe(rets20),
        float(np.mean(turns20)) if turns20 else 0.0,
        float(np.mean(ind20)) if ind20 else 0.0,
        float(np.mean(size20)) if size20 else 0.0,
        1.0 if method == "lingxi" else 0.0,
        1.0 if method == "lingxi_pitnorm" else 0.0,
        1.0 if method == "lingxi_pitnorm_gate_return_floor" else 0.0,
    ]


def reward_at(series: dict[str, list[dict]], idx: int, method: str, previous: str | None, args: argparse.Namespace) -> float:
    row = series[method][idx]
    switch_cost = args.switch_penalty if previous and previous != method else 0.0
    return float(row["net_return"] - args.turnover_penalty * row["turnover"] * 0.001 - switch_cost)


def make_static_ensemble(dates: list[str], series: dict[str, list[dict]]) -> list[dict]:
    rows = []
    weights = {method: 1.0 / len(METHODS) for method in METHODS}
    for idx, date in enumerate(dates):
        method_returns = {method: series[method][idx] for method in METHODS}
        rows.append(combine_row(date, method_returns, weights, "equal", False))
    return rows


def make_oracle(dates: list[str], series: dict[str, list[dict]]) -> list[dict]:
    rows = []
    previous = None
    for idx, date in enumerate(dates):
        selected = max(METHODS, key=lambda method: series[method][idx]["net_return"])
        weights = {method: 1.0 if method == selected else 0.0 for method in METHODS}
        method_returns = {method: series[method][idx] for method in METHODS}
        rows.append(combine_row(date, method_returns, weights, selected, previous is not None and previous != selected))
        previous = selected
    return rows


def make_rolling_selector(dates: list[str], series: dict[str, list[dict]], args: argparse.Namespace) -> list[dict]:
    rows = []
    previous = None
    for idx, date in enumerate(dates):
        selected = "lingxi"
        end = idx - args.horizon
        if end >= args.min_history:
            start = max(0, end - args.window)
            scores = {}
            for method in METHODS:
                returns = history_slice(series, method, start, end, "net_return")
                turnovers = history_slice(series, method, start, end, "turnover")
                score = rolling_metric(returns, turnovers, args)
                if previous and previous != method:
                    score -= args.switch_penalty
                scores[method] = score
            selected = max(scores, key=scores.get)
        weights = {method: 1.0 if method == selected else 0.0 for method in METHODS}
        method_returns = {method: series[method][idx] for method in METHODS}
        rows.append(combine_row(date, method_returns, weights, selected, previous is not None and previous != selected))
        previous = selected
    return rows


def make_hedge_router(dates: list[str], series: dict[str, list[dict]], args: argparse.Namespace) -> list[dict]:
    rows = []
    weights_raw = {method: 1.0 for method in METHODS}
    updated_until = -1
    for idx, date in enumerate(dates):
        while updated_until < idx - args.horizon:
            updated_until += 1
            for method in METHODS:
                reward = reward_at(series, updated_until, method, None, args)
                weights_raw[method] *= math.exp(args.hedge_eta * max(-0.05, min(0.05, reward)))
            total_raw = sum(weights_raw.values())
            if total_raw <= 0 or not math.isfinite(total_raw):
                weights_raw = {method: 1.0 for method in METHODS}
        total = sum(weights_raw.values())
        weights = {method: weights_raw[method] / total for method in METHODS}
        selected = max(weights, key=weights.get)
        method_returns = {method: series[method][idx] for method in METHODS}
        rows.append(combine_row(date, method_returns, weights, selected, False))
    return rows


def fit_ridge(xs: list[list[float]], ys: list[float], alpha: float) -> np.ndarray:
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    scale = np.std(x, axis=0)
    scale[scale <= 1e-12] = 1.0
    x_scaled = x / scale
    reg = alpha * np.eye(x_scaled.shape[1])
    reg[0, 0] = 0.0
    coef = np.linalg.solve(x_scaled.T @ x_scaled + reg, x_scaled.T @ y)
    return coef / scale


def make_contextual_ridge_router(dates: list[str], series: dict[str, list[dict]], args: argparse.Namespace) -> list[dict]:
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
            for method in METHODS:
                xs = [context_features(series, j, method, args) for j in range(train_start, train_end)]
                ys = [reward_at(series, j, method, None, args) for j in range(train_start, train_end)]
                if len(xs) >= args.min_history:
                    try:
                        coef = fit_ridge(xs, ys, args.ridge_alpha)
                        pred = float(np.dot(context_features(series, idx, method, args), coef))
                    except np.linalg.LinAlgError:
                        pred = float(np.mean(ys))
                    if previous and previous != method:
                        pred -= args.switch_penalty
                    predictions[method] = pred
            if predictions:
                selected = max(predictions, key=predictions.get)
                cached_selected = selected
        weights = {method: 1.0 if method == selected else 0.0 for method in METHODS}
        method_returns = {method: series[method][idx] for method in METHODS}
        rows.append(combine_row(date, method_returns, weights, selected, previous is not None and previous != selected))
        previous = selected
    return rows


def summarize(method: str, market: str, topk: int, variant: str, rows: list[dict], daily_path: Path) -> dict[str, str]:
    stats = performance_stats(rows, "net_return")
    active_stats = performance_stats(rows, "net_active_return")
    switch_rate = float(np.mean([row.get("switch", 0.0) for row in rows])) if rows else 0.0
    selected_counts: dict[str, int] = {}
    for row in rows:
        selected = str(row.get("selected_method", method))
        selected_counts[selected] = selected_counts.get(selected, 0) + 1
    years = sorted(set(row["date"][:4] for row in rows))
    yearly = []
    for year in years:
        year_rows = [row for row in rows if row["date"].startswith(year)]
        yearly.append((year, performance_stats(year_rows, "net_return")["ann_return"]))
    return {
        "market": market,
        "method": method,
        "method_label": METHOD_LABELS.get(method, method),
        "variant": variant,
        "horizon": "5",
        "topk": str(topk),
        "days": str(len(rows)),
        "ann_return": f"{stats['ann_return']:.8f}",
        "ann_vol": f"{stats['ann_vol']:.8f}",
        "sharpe": f"{stats['sharpe']:.8f}",
        "mdd": f"{stats['mdd']:.8f}",
        "cum_return": f"{stats['cum_return']:.8f}",
        "active_ann_return": f"{active_stats['ann_return']:.8f}",
        "active_sharpe": f"{active_stats['sharpe']:.8f}",
        "avg_turnover": f"{stats['avg_turnover']:.8f}",
        "hit_rate": f"{stats['hit_rate']:.8f}",
        "switch_rate": f"{switch_rate:.8f}",
        "selected_counts": ";".join(f"{key}:{value}" for key, value in sorted(selected_counts.items())),
        "yearly_ann_returns": ";".join(f"{year}:{value:.4f}" for year, value in yearly),
        "daily_source": str(daily_path.relative_to(PROJECT_ROOT)),
    }


def write_summary(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_router_daily(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "date",
        "selected_method",
        "net_return",
        "benchmark_return",
        "net_active_return",
        "turnover",
        "cost",
        "max_industry_weight",
        "size_exposure",
        "switch",
        "weight_lingxi",
        "weight_lingxi_pitnorm",
        "weight_lingxi_pitnorm_gate_return_floor",
    ]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    source_dir = resolve(args.source_dir)
    out_dir = resolve(args.out_dir)
    markets = args.market or MARKETS
    topks = sorted(set(args.topk or [10, 5]), reverse=True)
    variants = args.variant or VARIANTS
    summary_rows: list[dict[str, str]] = []

    for market in markets:
        for topk in topks:
            for variant in variants:
                dates, series = align_methods(source_dir, market, topk, variant)
                outputs = {
                    "static_equal_ensemble": make_static_ensemble(dates, series),
                    "rolling_selector": make_rolling_selector(dates, series, args),
                    "hedge_router": make_hedge_router(dates, series, args),
                    "contextual_ridge_router": make_contextual_ridge_router(dates, series, args),
                    "oracle_upper_bound": make_oracle(dates, series),
                }
                for method in METHODS:
                    outputs[method] = []
                    for idx, date in enumerate(dates):
                        weights = {name: 1.0 if name == method else 0.0 for name in METHODS}
                        method_returns = {name: series[name][idx] for name in METHODS}
                        outputs[method].append(combine_row(date, method_returns, weights, method, False))

                for method, rows in outputs.items():
                    daily_path = out_dir / market / f"{method}_h5_top{topk}_{variant}_daily.csv"
                    write_router_daily(daily_path, rows)
                    summary = summarize(method, market, topk, variant, rows, daily_path)
                    summary_rows.append(summary)
                    print(market, f"top{topk}", variant, method, summary["ann_return"], summary["sharpe"], summary["mdd"])

    write_summary(out_dir / "lingxi_adaptive_router_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'lingxi_adaptive_router_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

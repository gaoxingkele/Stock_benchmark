"""Validate sparse feature-selected market-regime routers for Lingxi."""

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=str(PROJECT_ROOT / "experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_sparse_regime_router_validation_2026_ytd"))
    parser.add_argument("--market", action="append", choices=base.MARKETS)
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--variant", action="append", choices=base.VARIANTS)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--min-history", type=int, default=30)
    parser.add_argument("--ridge-alpha", type=float, default=3.0)
    parser.add_argument("--ridge-refit-step", type=int, default=5)
    parser.add_argument("--turnover-penalty", type=float, default=0.15)
    parser.add_argument("--switch-penalty", type=float, default=0.00025)
    parser.add_argument("--max-features", type=int, default=20)
    parser.add_argument("--min-feature-corr", type=float, default=0.0)
    return parser.parse_args()


def feature_corrs(xs: list[list[float]], ys: list[float]) -> list[float]:
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    out = []
    y_std = float(np.std(y))
    for idx in range(x.shape[1]):
        column = x[:, idx]
        x_std = float(np.std(column))
        if idx == 0 or x_std <= 1e-12 or y_std <= 1e-12:
            out.append(0.0)
        else:
            value = float(np.corrcoef(column, y)[0, 1])
            out.append(value if np.isfinite(value) else 0.0)
    return out


def select_features(xs: list[list[float]], ys: list[float], args: argparse.Namespace) -> list[int]:
    corrs = feature_corrs(xs, ys)
    ranked = sorted(range(1, len(corrs)), key=lambda idx: abs(corrs[idx]), reverse=True)
    selected = [idx for idx in ranked if abs(corrs[idx]) >= args.min_feature_corr][: args.max_features]
    return [0, *selected]


def subset(rows: list[list[float]], indices: list[int]) -> list[list[float]]:
    return [[row[idx] for idx in indices] for row in rows]


def make_sparse_regime_router(
    dates: list[str],
    series: dict[str, list[dict]],
    regime: dict[str, dict[str, float]],
    args: argparse.Namespace,
    diagnostics_path: Path,
) -> list[dict]:
    rows = []
    diagnostics = []
    previous = None
    cached_selected = "lingxi"
    cached_feature_counts = {method: 0 for method in base.METHODS}
    for idx, date in enumerate(dates):
        selected = cached_selected
        train_end = idx - args.horizon
        should_refit = idx < args.min_history + args.horizon or idx % max(1, args.ridge_refit_step) == 0
        if should_refit and train_end >= args.min_history:
            train_start = max(args.horizon, train_end - args.window * 3)
            predictions = {}
            for method in base.METHODS:
                xs = [regime_base.context_features(series, regime, dates, j, method, args) for j in range(train_start, train_end)]
                ys = [base.reward_at(series, j, method, None, args) for j in range(train_start, train_end)]
                if len(xs) >= args.min_history:
                    selected_features = select_features(xs, ys, args)
                    cached_feature_counts[method] = len(selected_features) - 1
                    try:
                        coef = base.fit_ridge(subset(xs, selected_features), ys, args.ridge_alpha)
                        now = [regime_base.context_features(series, regime, dates, idx, method, args)[feature] for feature in selected_features]
                        pred = float(np.dot(now, coef))
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
        diagnostics.append(
            {
                "date": date,
                "selected_method": selected,
                **{f"feature_count_{method}": str(cached_feature_counts[method]) for method in base.METHODS},
            }
        )
        previous = selected

    diagnostics_path.parent.mkdir(parents=True, exist_ok=True)
    with diagnostics_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(diagnostics[0]))
        writer.writeheader()
        writer.writerows(diagnostics)
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
    labels = {
        **base.METHOD_LABELS,
        "contextual_ridge_router": "Contextual ridge router",
        "market_regime_ridge_router": "Market-regime ridge router",
        "sparse_regime_ridge_router": "Sparse market-regime ridge router",
    }
    summary_rows: list[dict[str, str]] = []

    for market in markets:
        regime = regime_base.read_panel_daily_features(regime_base.PANEL_PATHS[market])
        for topk in topks:
            for variant in variants:
                dates, series = base.align_methods(source_dir, market, topk, variant)
                diagnostics_path = out_dir / market / f"sparse_regime_ridge_router_h5_top{topk}_{variant}_diagnostics.csv"
                outputs = {
                    "static_equal_ensemble": base.make_static_ensemble(dates, series),
                    "contextual_ridge_router": base.make_contextual_ridge_router(dates, series, args),
                    "market_regime_ridge_router": regime_base.make_regime_ridge_router(dates, series, regime, args),
                    "sparse_regime_ridge_router": make_sparse_regime_router(dates, series, regime, args, diagnostics_path),
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

    write_summary(out_dir / "lingxi_sparse_regime_router_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'lingxi_sparse_regime_router_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

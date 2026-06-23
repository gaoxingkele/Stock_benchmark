"""Validate a frozen validation-only meta-selector for Lingxi routers."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import run_lingxi_adaptive_router_validation as base  # noqa: E402
from run_trade_validation import performance_stats  # noqa: E402


CANDIDATE_METHODS = [
    "lingxi",
    "lingxi_pitnorm",
    "lingxi_pitnorm_gate_return_floor",
    "static_equal_ensemble",
    "contextual_ridge_router",
    "market_regime_ridge_router",
    "sparse_regime_ridge_router",
]
REFERENCE_METHODS = ["oracle_upper_bound"]
METHOD_LABELS = {
    **base.METHOD_LABELS,
    "market_regime_ridge_router": "Market-regime ridge router",
    "sparse_regime_ridge_router": "Sparse market-regime ridge router",
    "validation_meta_selector": "Validation-only meta-selector",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=str(PROJECT_ROOT / "experiments/lingxi_sparse_regime_router_validation_2026_ytd"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_meta_selector_validation"))
    parser.add_argument("--market", action="append", choices=base.MARKETS)
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--variant", action="append", choices=base.VARIANTS)
    parser.add_argument("--validation-start", default="2023-01-01")
    parser.add_argument("--validation-end", default="2024-12-31")
    parser.add_argument("--oos-start", default="2025-01-01")
    parser.add_argument("--oos-end", default="2026-12-31")
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def read_daily(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as file:
        rows = []
        for row in csv.DictReader(file):
            rows.append(
                {
                    "date": row["date"],
                    "selected_method": row.get("selected_method", ""),
                    "net_return": float(row["net_return"]),
                    "benchmark_return": float(row.get("benchmark_return", 0.0)),
                    "net_active_return": float(row.get("net_active_return", 0.0)),
                    "turnover": float(row.get("turnover", 0.0)),
                    "cost": float(row.get("cost", 0.0)),
                    "max_industry_weight": float(row.get("max_industry_weight", 0.0)),
                    "size_exposure": float(row.get("size_exposure", 0.0)),
                    "switch": float(row.get("switch", 0.0)),
                    "weight_lingxi": float(row.get("weight_lingxi", 0.0)),
                    "weight_lingxi_pitnorm": float(row.get("weight_lingxi_pitnorm", 0.0)),
                    "weight_lingxi_pitnorm_gate_return_floor": float(row.get("weight_lingxi_pitnorm_gate_return_floor", 0.0)),
                }
            )
        return rows


def filter_dates(rows: list[dict], start: str, end: str) -> list[dict]:
    return [row for row in rows if start <= row["date"] <= end]


def summarize_rows(
    method: str,
    market: str,
    topk: int,
    variant: str,
    period: str,
    rows: list[dict],
    daily_path: Path,
    selected_by_validation: str = "",
) -> dict[str, str]:
    stats = performance_stats(rows, "net_return")
    active_stats = performance_stats(rows, "net_active_return")
    years = sorted(set(row["date"][:4] for row in rows))
    yearly = []
    for year in years:
        year_rows = [row for row in rows if row["date"].startswith(year)]
        yearly.append((year, performance_stats(year_rows, "net_return")["ann_return"]))
    return {
        "market": market,
        "method": method,
        "method_label": METHOD_LABELS.get(method, method),
        "selected_by_validation": selected_by_validation,
        "period": period,
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
        "switch_rate": f"{sum(float(row.get('switch', 0.0)) for row in rows) / len(rows):.8f}" if rows else "0.00000000",
        "yearly_ann_returns": ";".join(f"{year}:{value:.4f}" for year, value in yearly),
        "daily_source": str(daily_path.relative_to(PROJECT_ROOT)),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
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
    selection_rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []

    periods = {
        "validation_2023_2024": (args.validation_start, args.validation_end),
        "oos_2025": ("2025-01-01", "2025-12-31"),
        "oos_2026_ytd": ("2026-01-01", args.oos_end),
        "oos_2025_2026_ytd": (args.oos_start, args.oos_end),
    }

    for market in markets:
        for topk in topks:
            for variant in variants:
                daily_by_method = {}
                for method in [*CANDIDATE_METHODS, *REFERENCE_METHODS]:
                    path = source_dir / market / f"{method}_h5_top{topk}_{variant}_daily.csv"
                    daily_by_method[method] = read_daily(path)

                validation_scores = {}
                for method in CANDIDATE_METHODS:
                    rows = filter_dates(daily_by_method[method], args.validation_start, args.validation_end)
                    validation_scores[method] = performance_stats(rows, "net_return")["sharpe"] if rows else float("-inf")
                selected = max(validation_scores, key=validation_scores.get)
                selection_rows.append(
                    {
                        "market": market,
                        "topk": str(topk),
                        "variant": variant,
                        "selected_method": selected,
                        "selected_label": METHOD_LABELS.get(selected, selected),
                        "validation_sharpe": f"{validation_scores[selected]:.8f}",
                        "all_validation_sharpes": ";".join(f"{method}:{validation_scores[method]:.6f}" for method in CANDIDATE_METHODS),
                    }
                )

                for period, (start, end) in periods.items():
                    candidate_methods = [selected, "static_equal_ensemble", "lingxi", "lingxi_pitnorm", "lingxi_pitnorm_gate_return_floor", "oracle_upper_bound"]
                    for method in dict.fromkeys(candidate_methods):
                        rows = filter_dates(daily_by_method[method], start, end)
                        if not rows:
                            continue
                        if method == selected:
                            meta_rows = [dict(row, selected_method=selected) for row in rows]
                            daily_path = out_dir / market / f"validation_meta_selector_h5_top{topk}_{variant}_{period}_daily.csv"
                            base.write_router_daily(daily_path, meta_rows)
                            summary_rows.append(
                                summarize_rows(
                                    "validation_meta_selector",
                                    market,
                                    topk,
                                    variant,
                                    period,
                                    meta_rows,
                                    daily_path,
                                    selected_by_validation=selected,
                                )
                            )
                        daily_path = source_dir / market / f"{method}_h5_top{topk}_{variant}_daily.csv"
                        summary_rows.append(summarize_rows(method, market, topk, variant, period, rows, daily_path))

                print(market, f"top{topk}", variant, "selected", selected, f"val_sharpe={validation_scores[selected]:.4f}")

    write_csv(out_dir / "lingxi_meta_selector_selection_table.csv", selection_rows)
    write_csv(out_dir / "lingxi_meta_selector_validation_summary.csv", summary_rows)
    print(f"selection={out_dir / 'lingxi_meta_selector_selection_table.csv'} rows={len(selection_rows)}")
    print(f"summary={out_dir / 'lingxi_meta_selector_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

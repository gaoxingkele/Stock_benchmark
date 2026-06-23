"""Frozen structured market-tag ablation for CASE-Lingxi.

This is an LLM-compatible tag ablation, not a live LLM trader. The script
creates point-in-time structured market tags from lagged market context, then
tests whether a tag-aware router can improve over the static production menu
and the conservative context router.

The generated tags are intentionally transparent so they can later be replaced
by timestamped multi-LLM debate outputs with the same schema.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import run_case_lingxi_context_router as context_base  # noqa: E402
import run_lingxi_adaptive_router_validation as base  # noqa: E402
import run_lingxi_regime_router_validation as regime_base  # noqa: E402


TAG_ROUTER_NAME = "case_lingxi_market_tag_router"
TAG_SCHEMA_VERSION = "case_lingxi_market_tags_v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", default=str(PROJECT_ROOT / "experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/case_lingxi_llm_tag_ablation_2026_ytd"))
    parser.add_argument("--market", action="append", choices=base.MARKETS)
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--variant", action="append", choices=base.VARIANTS)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--min-history", type=int, default=30)
    parser.add_argument("--risk-aversion", type=float, default=0.35)
    parser.add_argument("--drawdown-penalty", type=float, default=0.10)
    parser.add_argument("--turnover-penalty", type=float, default=0.15)
    parser.add_argument("--switch-penalty", type=float, default=0.00025)
    parser.add_argument("--risk-drawdown", type=float, default=-0.05)
    parser.add_argument("--vol-lookback", type=int, default=120)
    parser.add_argument("--vol-quantile", type=float, default=0.75)
    parser.add_argument("--switch-margin", type=float, default=0.00015)
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def training_thresholds(regime: dict[str, dict[str, float]], dates: list[str]) -> dict[str, float]:
    values = {
        "vol20": [float(regime[date].get("vol20", 0.0)) for date in dates if date in regime],
        "dispersion20": [float(regime[date].get("dispersion20", 0.0)) for date in dates if date in regime],
        "breadth20": [float(regime[date].get("breadth20", 0.5)) for date in dates if date in regime],
    }
    return {
        "vol20_q70": float(np.quantile(values["vol20"], 0.70)) if values["vol20"] else 0.0,
        "dispersion20_q70": float(np.quantile(values["dispersion20"], 0.70)) if values["dispersion20"] else 0.0,
        "breadth20_q40": float(np.quantile(values["breadth20"], 0.40)) if values["breadth20"] else 0.45,
    }


def tag_for_row(row: dict[str, float], thresholds: dict[str, float]) -> dict[str, str]:
    mom20 = float(row.get("mom20", 0.0))
    mom60 = float(row.get("mom60", 0.0))
    vol20 = float(row.get("vol20", 0.0))
    drawdown60 = float(row.get("drawdown60", 0.0))
    breadth20 = float(row.get("breadth20", 0.5))
    dispersion20 = float(row.get("dispersion20", 0.0))

    trend = "up" if mom20 > 0 and mom60 > 0 else "down" if mom20 < 0 and mom60 < 0 else "mixed"
    volatility = "high" if vol20 >= thresholds["vol20_q70"] else "normal"
    drawdown = "stress" if drawdown60 <= -0.05 else "watch" if drawdown60 <= -0.025 else "calm"
    breadth = "weak" if breadth20 <= thresholds["breadth20_q40"] else "broad"
    dispersion = "high" if dispersion20 >= thresholds["dispersion20_q70"] else "normal"

    if drawdown == "stress" and volatility == "high":
        llm_style_summary = "risk_off_stress"
    elif trend == "up" and breadth == "broad" and volatility == "normal":
        llm_style_summary = "risk_on_trend"
    elif dispersion == "high" and trend != "down":
        llm_style_summary = "selective_alpha"
    elif trend == "down" and breadth == "weak":
        llm_style_summary = "defensive"
    else:
        llm_style_summary = "balanced"

    return {
        "trend_tag": trend,
        "volatility_tag": volatility,
        "drawdown_tag": drawdown,
        "breadth_tag": breadth,
        "dispersion_tag": dispersion,
        "llm_style_summary": llm_style_summary,
    }


def build_market_tags(
    regime: dict[str, dict[str, float]],
    dates: list[str],
    args: argparse.Namespace,
) -> dict[str, dict[str, str]]:
    train_dates = [date for date in dates if date <= "2024-12-31"]
    thresholds = training_thresholds(regime, train_dates or dates)
    tags: dict[str, dict[str, str]] = {}
    for idx, date in enumerate(dates):
        end = idx - args.horizon
        if end <= 0:
            row = {}
        else:
            row = regime.get(dates[end], {})
        tags[date] = {
            "date": date,
            "schema_version": TAG_SCHEMA_VERSION,
            "source": "deterministic_lagged_context_proxy_for_llm_tags",
            "lag_days": str(args.horizon),
            **tag_for_row(row, thresholds),
        }
    return tags


def write_tags(path: Path, tags: dict[str, dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [tags[date] for date in sorted(tags)]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def preferred_sleeves_for_tag(market: str, variant: str, tag: dict[str, str]) -> list[str]:
    summary = tag["llm_style_summary"]
    if summary in {"risk_off_stress", "defensive"}:
        if market == "crypto_major" and variant == "raw":
            return ["lingxi_pitnorm", "lingxi_pitnorm_gate_return_floor", "lingxi"]
        return ["lingxi_pitnorm", "lingxi_pitnorm_gate_return_floor", "lingxi"]
    if summary == "risk_on_trend":
        if market == "crypto_major" and variant == "raw":
            return ["lingxi_pitnorm_gate_return_floor", "lingxi", "lingxi_pitnorm"]
        return ["lingxi", "lingxi_pitnorm_gate_return_floor", "lingxi_pitnorm"]
    if summary == "selective_alpha":
        return ["lingxi", "lingxi_pitnorm_gate_return_floor", "lingxi_pitnorm"]
    return [context_base.production_menu_method(market, 10, variant), "lingxi", "lingxi_pitnorm", "lingxi_pitnorm_gate_return_floor"]


def tag_adjusted_score(base_score: float, method: str, tag: dict[str, str], market: str, variant: str) -> float:
    summary = tag["llm_style_summary"]
    adjustment = 0.0
    if summary in {"risk_off_stress", "defensive"}:
        if method == "lingxi_pitnorm":
            adjustment += 0.00020
        if method == "lingxi":
            adjustment -= 0.00015
    elif summary == "risk_on_trend":
        if method == "lingxi":
            adjustment += 0.00020
        if method == "lingxi_pitnorm":
            adjustment -= 0.00010
    elif summary == "selective_alpha":
        if method == "lingxi":
            adjustment += 0.00010
    if market == "crypto_major" and variant == "raw" and method == "lingxi_pitnorm_gate_return_floor":
        adjustment += 0.00010
    return base_score + adjustment


def make_tag_router_rows(
    dates: list[str],
    series: dict[str, list[dict]],
    tags: dict[str, dict[str, str]],
    market: str,
    topk: int,
    variant: str,
    args: argparse.Namespace,
) -> list[dict]:
    rows = []
    previous = None
    default_method = context_base.production_menu_method(market, topk, variant)
    for idx, date in enumerate(dates):
        tag = tags[date]
        candidates = list(dict.fromkeys([method for method in preferred_sleeves_for_tag(market, variant, tag) if method in base.METHODS]))
        if default_method not in candidates:
            candidates.append(default_method)
        scores = {}
        for method in candidates:
            score = context_base.lagged_score(series, method, idx, args)
            scores[method] = tag_adjusted_score(score, method, tag, market, variant)
        selected = max(scores, key=scores.get) if scores else default_method
        if previous and previous != selected:
            selected_score = scores.get(selected, -1e9) - args.switch_penalty
            previous_score = scores.get(previous, context_base.lagged_score(series, previous, idx, args))
            if previous_score >= selected_score:
                selected = previous
        weights = {method: 1.0 if method == selected else 0.0 for method in base.METHODS}
        method_returns = {method: series[method][idx] for method in base.METHODS}
        row = base.combine_row(date, method_returns, weights, selected, previous is not None and previous != selected)
        row["tag_summary"] = tag["llm_style_summary"]
        rows.append(row)
        previous = selected
    return rows


def write_router_daily_with_tags(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "date",
        "selected_method",
        "tag_summary",
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


def write_summary(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summarize_tag_counts(rows: list[dict]) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        tag = str(row.get("tag_summary", "none"))
        counts[tag] = counts.get(tag, 0) + 1
    return ";".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def main() -> int:
    args = parse_args()
    source_dir = resolve(args.source_dir)
    out_dir = resolve(args.out_dir)
    markets = args.market or base.MARKETS
    topks = sorted(set(args.topk or [10, 5]), reverse=True)
    variants = args.variant or base.VARIANTS
    labels = {
        **base.METHOD_LABELS,
        context_base.MENU_NAME: "CASE-Lingxi static production menu",
        context_base.ROUTER_NAME: "CASE-Lingxi conservative context router",
        TAG_ROUTER_NAME: "CASE-Lingxi structured market-tag router",
    }
    summary_rows: list[dict[str, str]] = []

    for market in markets:
        regime = regime_base.read_panel_daily_features(regime_base.PANEL_PATHS[market])
        for topk in topks:
            for variant in variants:
                dates, series = base.align_methods(source_dir, market, topk, variant)
                tags = build_market_tags(regime, dates, args)
                tag_path = out_dir / market / f"market_tags_h5_top{topk}_{variant}.csv"
                write_tags(tag_path, tags)

                outputs = {
                    context_base.MENU_NAME: context_base.make_static_menu_rows(dates, series, market, topk, variant),
                    context_base.ROUTER_NAME: context_base.make_context_router_rows(dates, series, regime, market, topk, variant, args),
                    TAG_ROUTER_NAME: make_tag_router_rows(dates, series, tags, market, topk, variant, args),
                    "static_equal_ensemble": base.make_static_ensemble(dates, series),
                    "oracle_upper_bound": base.make_oracle(dates, series),
                }
                for method in base.METHODS:
                    outputs[method] = context_base.make_fixed_method_rows(dates, series, method)

                for method, rows in outputs.items():
                    daily_path = out_dir / market / f"{method}_h5_top{topk}_{variant}_daily.csv"
                    if method == TAG_ROUTER_NAME:
                        write_router_daily_with_tags(daily_path, rows)
                    else:
                        base.write_router_daily(daily_path, rows)
                    summary = base.summarize(method, market, topk, variant, rows, daily_path)
                    summary["method_label"] = labels.get(method, method)
                    summary["tag_schema"] = TAG_SCHEMA_VERSION if method == TAG_ROUTER_NAME else ""
                    summary["tag_counts"] = summarize_tag_counts(rows) if method == TAG_ROUTER_NAME else ""
                    summary["tag_source"] = str(tag_path.relative_to(PROJECT_ROOT)) if method == TAG_ROUTER_NAME else ""
                    summary_rows.append(summary)
                    print(market, f"top{topk}", variant, method, summary["ann_return"], summary["sharpe"], summary["mdd"])

    write_summary(out_dir / "case_lingxi_llm_tag_ablation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'case_lingxi_llm_tag_ablation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Validate return-floor and market-aware PITNorm gates for Lingxi."""

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

import run_lingxi_topk_comparison as topk_comparison  # noqa: E402
from run_lingxi_fusion_validation import MARKETS  # noqa: E402
from run_lingxi_sota_upgrade_validation import make_pitnorm_scores  # noqa: E402
from run_lingxi_topk_comparison import add_lingxi_neutral_scores, build_lingxi_scores, summarize_daily  # noqa: E402


topk_comparison.MARKETS.update(MARKETS)

METHOD_LABELS = {
    "lingxi": "Lingxi / RDA-Adapt",
    "lingxi_pitnorm": "Lingxi-PITNorm",
    "lingxi_pitnorm_gate_return_floor": "Lingxi-PITNorm ReturnFloor-Gate",
    "lingxi_pitnorm_gate_hk_bias": "Lingxi-PITNorm ReturnFloor-HKBias-Gate",
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
    parser.add_argument("--max-train-rows", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--gate-weights", default="0,0.5,1.0")
    parser.add_argument("--gate-window", type=int, default=40)
    parser.add_argument("--gate-min-history", type=int, default=20)
    parser.add_argument("--risk-aversion", type=float, default=0.35)
    parser.add_argument("--drawdown-penalty", type=float, default=0.10)
    parser.add_argument("--turnover-penalty", type=float, default=0.20)
    parser.add_argument("--return-floor-ratio", type=float, default=0.85)
    parser.add_argument("--return-floor-penalty", type=float, default=2.0)
    parser.add_argument("--hk-pitnorm-bias", type=float, default=0.00025)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_pitnorm_tuned_gate_validation"))
    return parser.parse_args()


def daily_z(rows: list[dict], field: str) -> dict[tuple[str, str], float]:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_date[row["date"]].append(row)
    out: dict[tuple[str, str], float] = {}
    for date_rows in by_date.values():
        values = np.asarray([float(row[field]) for row in date_rows], dtype=float)
        finite = np.isfinite(values)
        if finite.any():
            center = float(np.nanmean(values[finite]))
            scale = float(np.nanstd(values[finite]))
            values = values - center if scale <= 1e-12 or not math.isfinite(scale) else (values - center) / scale
            values[~finite] = 0.0
        else:
            values = np.zeros(len(date_rows), dtype=float)
        for row, value in zip(date_rows, values):
            out[(row["date"], row["symbol"])] = float(value)
    return out


def keyed(rows: list[dict]) -> dict[tuple[str, str], dict]:
    return {(row["date"], row["symbol"]): row for row in rows}


def max_drawdown(values: list[float]) -> float:
    nav = 1.0
    peak = 1.0
    worst = 0.0
    for value in values:
        nav *= 1.0 + value
        peak = max(peak, nav)
        worst = min(worst, nav / peak - 1.0)
    return worst


def candidate_metric(
    rows: list[dict],
    weight: float,
    previous: set[str],
    topk: int,
    horizon: int,
    cost_bps: float,
    base_field: str,
    pit_field: str,
) -> tuple[float, float, set[str]]:
    ranked = sorted(rows, key=lambda row: (1.0 - weight) * float(row[base_field]) + weight * float(row[pit_field]), reverse=True)
    selected = ranked[:topk]
    if len(selected) < topk:
        return 0.0, 0.0, previous
    symbols = {str(row["symbol"]) for row in selected}
    turnover = 0.5 * (len(symbols - previous) + len(previous - symbols)) / topk if previous else 0.5
    gross = float(np.mean([float(row["label"]) for row in selected]) / horizon)
    return gross - turnover * (cost_bps / 10000.0), turnover, symbols


def build_date_rows(lingxi_rows: list[dict], pitnorm_rows: list[dict]) -> dict[str, list[dict]]:
    base = keyed(lingxi_rows)
    pit = keyed(pitnorm_rows)
    fields = {
        "lingxi_raw_z": daily_z(lingxi_rows, "score"),
        "pitnorm_raw_z": daily_z(pitnorm_rows, "score"),
        "lingxi_neutral_z": daily_z(lingxi_rows, "neutral_score"),
        "pitnorm_neutral_z": daily_z(pitnorm_rows, "neutral_score"),
    }
    by_date: dict[str, list[dict]] = defaultdict(list)
    for key in sorted(set(base) & set(pit)):
        row = base[key]
        by_date[key[0]].append(
            {
                "date": row["date"],
                "symbol": row["symbol"],
                "label": float(row["label"]),
                "industry": row.get("industry", "UNKNOWN"),
                "total_mv": float(row.get("total_mv", float("nan"))),
                **{name: values[key] for name, values in fields.items()},
            }
        )
    return by_date


def make_variant_gate_scores(
    by_date: dict[str, list[dict]],
    market: str,
    variant: str,
    topk: int,
    args: argparse.Namespace,
    diagnostics_path: Path,
    hk_bias: bool,
) -> list[dict]:
    base_field = "lingxi_raw_z" if variant == "raw" else "lingxi_neutral_z"
    pit_field = "pitnorm_raw_z" if variant == "raw" else "pitnorm_neutral_z"
    dates = sorted(by_date)
    weights = sorted({float(item.strip()) for item in args.gate_weights.split(",") if item.strip()} | {0.0})
    history: dict[float, dict[str, list[float]]] = {weight: {"ret": [], "turnover": []} for weight in weights}
    previous: dict[float, set[str]] = {weight: set() for weight in weights}
    chosen_by_date: dict[str, float] = {}
    diagnostics: list[dict[str, str]] = []

    for idx, date in enumerate(dates):
        usable_end = idx - args.horizon
        best_weight = 0.0
        best_score = float("-inf")
        baseline_mean = 0.0
        if usable_end >= args.gate_min_history:
            start = max(0, usable_end - args.gate_window)
            baseline_returns = history[0.0]["ret"][start:usable_end]
            baseline_mean = float(np.mean(baseline_returns)) if baseline_returns else 0.0
            floor = baseline_mean * args.return_floor_ratio if baseline_mean > 0 else baseline_mean
            for weight in weights:
                returns = history[weight]["ret"][start:usable_end]
                turnovers = history[weight]["turnover"][start:usable_end]
                if len(returns) < args.gate_min_history:
                    continue
                mean = float(np.mean(returns))
                vol = float(np.std(returns))
                drawdown = abs(max_drawdown(returns))
                turnover = float(np.mean(turnovers)) if turnovers else 0.0
                score = mean - args.risk_aversion * vol - args.drawdown_penalty * drawdown / max(len(returns), 1)
                score -= args.turnover_penalty * turnover * (args.cost_bps / 10000.0)
                if mean < floor:
                    score -= args.return_floor_penalty * (floor - mean)
                if hk_bias and market == "hk_large_cap" and weight > 0:
                    score += args.hk_pitnorm_bias * weight
                if score > best_score:
                    best_score = score
                    best_weight = weight
        chosen_by_date[date] = best_weight

        for weight in weights:
            ret, turnover, symbols = candidate_metric(by_date[date], weight, previous[weight], topk, args.horizon, args.cost_bps, base_field, pit_field)
            history[weight]["ret"].append(ret)
            history[weight]["turnover"].append(turnover)
            previous[weight] = symbols

        diagnostics.append(
            {
                "date": date,
                "variant": variant,
                "topk": str(topk),
                "chosen_pitnorm_weight": f"{best_weight:.6f}",
                "baseline_mean": f"{baseline_mean:.8f}",
                "history_days": str(max(0, min(args.gate_window, usable_end))),
                "hk_bias": str(hk_bias),
            }
        )

    out: list[dict] = []
    for date in dates:
        weight = chosen_by_date[date]
        for row in sorted(by_date[date], key=lambda item: str(item["symbol"])):
            score = (1.0 - weight) * float(row[base_field]) + weight * float(row[pit_field])
            out.append(
                {
                    "date": row["date"],
                    "symbol": row["symbol"],
                    "score": float(score),
                    "label": float(row["label"]),
                    "industry": row.get("industry", "UNKNOWN"),
                    "total_mv": float(row.get("total_mv", float("nan"))),
                }
            )
    add_lingxi_neutral_scores(out)
    diagnostics_path.parent.mkdir(parents=True, exist_ok=True)
    with diagnostics_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(diagnostics[0]))
        writer.writeheader()
        writer.writerows(diagnostics)
    return out


def write_summary(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    markets = args.market or ["cn_a_share", "us_large_cap", "hk_large_cap", "crypto_major"]
    requested_topks = sorted(set(args.topk or [5, 10]), reverse=True)
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir
    summary_rows: list[dict[str, str]] = []

    for market in markets:
        config = MARKETS[market]
        args.valid_start = config["valid_start"]
        panel = config["panel"]
        stock_basic = config["stock_basic"]
        topks = [topk for topk in requested_topks if topk <= int(config.get("max_topk", topk))]
        lingxi = build_lingxi_scores(args, market, panel, stock_basic)
        pitnorm = make_pitnorm_scores(lingxi)
        by_date = build_date_rows(lingxi, pitnorm)
        for topk in topks:
            for variant in ["raw", "industry_size_neutral"]:
                score_field = "score" if variant == "raw" else "neutral_score"
                candidates = {
                    "lingxi": lingxi,
                    "lingxi_pitnorm": pitnorm,
                    "lingxi_pitnorm_gate_return_floor": make_variant_gate_scores(
                        by_date,
                        market,
                        variant,
                        topk,
                        args,
                        out_dir / market / f"return_floor_h{args.horizon}_top{topk}_{variant}_diagnostics.csv",
                        hk_bias=False,
                    ),
                    "lingxi_pitnorm_gate_hk_bias": make_variant_gate_scores(
                        by_date,
                        market,
                        variant,
                        topk,
                        args,
                        out_dir / market / f"hk_bias_h{args.horizon}_top{topk}_{variant}_diagnostics.csv",
                        hk_bias=True,
                    ),
                }
                for method, rows in candidates.items():
                    row = summarize_daily(out_dir, market, method, topk, variant, score_field, rows, args)
                    row["method_label"] = METHOD_LABELS[method]
                    summary_rows.append(row)
                    print(market, method, f"top{topk}", variant, row["ann_return"], row["sharpe"], row["mdd"])

    write_summary(out_dir / "lingxi_pitnorm_tuned_gate_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'lingxi_pitnorm_tuned_gate_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

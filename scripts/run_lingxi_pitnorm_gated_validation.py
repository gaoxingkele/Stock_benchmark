"""Validate online gating between Lingxi and Lingxi-PITNorm."""

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
    "lingxi_pitnorm_gate": "Lingxi-PITNorm-Gate",
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
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_pitnorm_gated_validation"))
    return parser.parse_args()


def daily_z(rows: list[dict], field: str = "score") -> dict[tuple[str, str], float]:
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
) -> tuple[float, float, set[str]]:
    ranked = sorted(rows, key=lambda row: (1.0 - weight) * float(row["lingxi_z"]) + weight * float(row["pitnorm_z"]), reverse=True)
    selected = ranked[:topk]
    if len(selected) < topk:
        return 0.0, 0.0, previous
    symbols = {str(row["symbol"]) for row in selected}
    turnover = 0.5 * (len(symbols - previous) + len(previous - symbols)) / topk if previous else 0.5
    gross = float(np.mean([float(row["label"]) for row in selected]) / horizon)
    return gross - turnover * (cost_bps / 10000.0), turnover, symbols


def make_gate_scores(
    lingxi_rows: list[dict],
    pitnorm_rows: list[dict],
    topk: int,
    args: argparse.Namespace,
    diagnostics_path: Path,
) -> list[dict]:
    base = keyed(lingxi_rows)
    pit = keyed(pitnorm_rows)
    lingxi_z = daily_z(lingxi_rows)
    pitnorm_z = daily_z(pitnorm_rows)
    keys = sorted(set(base) & set(pit))
    by_date: dict[str, list[dict]] = defaultdict(list)
    for key in keys:
        row = base[key]
        by_date[key[0]].append(
            {
                "date": row["date"],
                "symbol": row["symbol"],
                "label": float(row["label"]),
                "industry": row.get("industry", "UNKNOWN"),
                "total_mv": float(row.get("total_mv", float("nan"))),
                "lingxi_z": lingxi_z[key],
                "pitnorm_z": pitnorm_z[key],
            }
        )

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
        if usable_end >= args.gate_min_history:
            start = max(0, usable_end - args.gate_window)
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
                if score > best_score:
                    best_score = score
                    best_weight = weight
        chosen_by_date[date] = best_weight

        for weight in weights:
            ret, turnover, symbols = candidate_metric(by_date[date], weight, previous[weight], topk, args.horizon, args.cost_bps)
            history[weight]["ret"].append(ret)
            history[weight]["turnover"].append(turnover)
            previous[weight] = symbols

        diagnostics.append(
            {
                "date": date,
                "topk": str(topk),
                "chosen_pitnorm_weight": f"{best_weight:.6f}",
                "history_days": str(max(0, min(args.gate_window, usable_end))),
                "candidate_weights": ";".join(f"{weight:.2f}" for weight in weights),
            }
        )

    out_rows: list[dict] = []
    for date in dates:
        weight = chosen_by_date[date]
        for row in sorted(by_date[date], key=lambda item: str(item["symbol"])):
            score = (1.0 - weight) * float(row["lingxi_z"]) + weight * float(row["pitnorm_z"])
            out_rows.append(
                {
                    "date": row["date"],
                    "symbol": row["symbol"],
                    "score": float(score),
                    "label": float(row["label"]),
                    "industry": row.get("industry", "UNKNOWN"),
                    "total_mv": float(row.get("total_mv", float("nan"))),
                }
            )
    add_lingxi_neutral_scores(out_rows)

    diagnostics_path.parent.mkdir(parents=True, exist_ok=True)
    with diagnostics_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(diagnostics[0]))
        writer.writeheader()
        writer.writerows(diagnostics)
    return out_rows


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
        market_topks = [topk for topk in requested_topks if topk <= int(config.get("max_topk", topk))]
        lingxi = build_lingxi_scores(args, market, panel, stock_basic)
        pitnorm = make_pitnorm_scores(lingxi)
        method_scores = {"lingxi": lingxi, "lingxi_pitnorm": pitnorm}
        for topk in market_topks:
            gated = make_gate_scores(
                lingxi,
                pitnorm,
                topk,
                args,
                out_dir / market / f"lingxi_pitnorm_gate_h{args.horizon}_top{topk}_diagnostics.csv",
            )
            method_scores[f"lingxi_pitnorm_gate_top{topk}"] = gated
            for method, scored_rows in [
                ("lingxi", lingxi),
                ("lingxi_pitnorm", pitnorm),
                ("lingxi_pitnorm_gate", gated),
            ]:
                for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
                    row = summarize_daily(out_dir, market, method, topk, variant, score_field, scored_rows, args)
                    row["method_label"] = METHOD_LABELS[method]
                    summary_rows.append(row)
                    print(market, method, f"top{topk}", variant, row["ann_return"], row["sharpe"], row["mdd"])

    write_summary(out_dir / "lingxi_pitnorm_gated_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'lingxi_pitnorm_gated_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

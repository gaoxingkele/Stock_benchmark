"""Validate Lingxi-Fusion variants that reuse runner-up algorithm strengths.

Fusion design:
- Lite: Lingxi backbone plus a small Qlib Alpha158 stabilizer.
- Regime: Lingxi backbone plus an online FinTSB adapter gate.
- Full: Lite backbone plus the same online FinTSB adapter gate.

The gate uses only lagged portfolio outcomes at least H trading days behind the
decision date.
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

import run_lingxi_topk_comparison as topk_comparison  # noqa: E402
from run_lingxi_topk_comparison import (  # noqa: E402
    MARKETS as BASE_MARKETS,
    RUNNER_METHODS,
    add_lingxi_neutral_scores,
    build_lingxi_scores,
    build_runner_scores,
    summarize_daily,
)


MARKETS = {
    **BASE_MARKETS,
    "crypto_major": {
        "panel": PROJECT_ROOT / "data/processed/global_markets/crypto_major_2018_2026/panel.csv",
        "stock_basic": PROJECT_ROOT / "data/processed/global_markets/crypto_major_2018_2026/stock_basic.csv",
        "valid_start": "2022-01-03",
        "max_topk": 20,
    },
}
topk_comparison.MARKETS.update(MARKETS)

METHOD_LABELS = {
    "lingxi": "Lingxi / RDA-Adapt",
    "qlib_alpha158": "Qlib Alpha158 proxy",
    "fintsb_ts": "FinTSB time-series proxy",
    "lingxi_fusion_lite": "Lingxi-Fusion-Lite",
    "lingxi_fusion_regime": "Lingxi-Fusion-Regime",
    "lingxi_fusion_full": "Lingxi-Fusion-Full",
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
    parser.add_argument("--qlib-weight", type=float, default=0.15)
    parser.add_argument("--gate-weights", default="0,0.10,0.25")
    parser.add_argument("--gate-window", type=int, default=40)
    parser.add_argument("--gate-min-history", type=int, default=20)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_fusion_validation"))
    return parser.parse_args()


def daily_z(rows: list[dict], field: str = "score") -> dict[tuple[str, str], float]:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_date[row["date"]].append(row)
    out: dict[tuple[str, str], float] = {}
    for date, date_rows in by_date.items():
        values = np.asarray([float(row[field]) for row in date_rows], dtype=float)
        finite = np.isfinite(values)
        if not finite.any():
            values = np.zeros(len(date_rows), dtype=float)
        else:
            center = float(np.nanmean(values[finite]))
            scale = float(np.nanstd(values[finite]))
            if scale <= 1e-12 or not math.isfinite(scale):
                values = values - center
            else:
                values = (values - center) / scale
            values[~finite] = 0.0
        for row, value in zip(date_rows, values):
            out[(date, row["symbol"])] = float(value)
    return out


def keyed(rows: list[dict]) -> dict[tuple[str, str], dict]:
    return {(row["date"], row["symbol"]): row for row in rows}


def clone_from(base: dict, score: float) -> dict:
    return {
        "date": base["date"],
        "symbol": base["symbol"],
        "score": float(score),
        "label": float(base["label"]),
        "industry": base.get("industry", "UNKNOWN"),
        "total_mv": float(base.get("total_mv", float("nan"))),
    }


def make_lite_scores(lingxi: list[dict], qlib: list[dict], qlib_weight: float) -> list[dict]:
    lmap = keyed(lingxi)
    qz = daily_z(qlib)
    lz = daily_z(lingxi)
    rows = [clone_from(base, lz[key] + qlib_weight * qz[key]) for key, base in sorted(lmap.items()) if key in qz]
    add_lingxi_neutral_scores(rows)
    return rows


def max_drawdown(values: list[float]) -> float:
    nav = 1.0
    peak = 1.0
    worst = 0.0
    for value in values:
        nav *= 1.0 + value
        peak = max(peak, nav)
        worst = min(worst, nav / peak - 1.0)
    return worst


def corr(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 3:
        return 0.0
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    if float(np.std(x)) <= 1e-12 or float(np.std(y)) <= 1e-12:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def candidate_metric(
    rows: list[dict],
    base_field: str,
    adapter_field: str,
    weight: float,
    previous: set[str],
    topk: int,
    horizon: int,
    cost_bps: float,
) -> tuple[float, float, set[str]]:
    ranked = sorted(
        rows,
        key=lambda row: (1.0 - weight) * float(row[base_field]) + weight * float(row[adapter_field]),
        reverse=True,
    )
    selected = ranked[:topk]
    if len(selected) < topk:
        return 0.0, 0.0, previous
    symbols = {str(row["symbol"]) for row in selected}
    turnover = 0.5 * (len(symbols - previous) + len(previous - symbols)) / topk if previous else 0.5
    gross = float(np.mean([float(row["label"]) for row in selected]) / horizon)
    return gross - turnover * (cost_bps / 10000.0), turnover, symbols


def gate_scores(
    base_rows: list[dict],
    adapter_rows: list[dict],
    topk: int,
    args: argparse.Namespace,
    diagnostics_path: Path,
) -> list[dict]:
    base_map = keyed(base_rows)
    adapter_z = daily_z(adapter_rows)
    base_z = daily_z(base_rows)
    keys = sorted(set(base_map) & set(adapter_z))
    by_date: dict[str, list[dict]] = defaultdict(list)
    for key in keys:
        base = base_map[key]
        by_date[key[0]].append(
            {
                **base,
                "base_z": base_z[key],
                "adapter_z": adapter_z[key],
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
        proxy_ic = adapter_ic = 0.0
        if usable_end >= args.gate_min_history:
            start = max(0, usable_end - args.gate_window)
            lagged = [row for past_date in dates[start:usable_end] for row in by_date[past_date]]
            labels = [float(row["label"]) for row in lagged]
            proxy_ic = corr([float(row["base_z"]) for row in lagged], labels)
            adapter_ic = corr([float(row["adapter_z"]) for row in lagged], labels)
            for weight in weights:
                returns = history[weight]["ret"][start:usable_end]
                turnovers = history[weight]["turnover"][start:usable_end]
                if len(returns) < args.gate_min_history:
                    continue
                mean = float(np.mean(returns))
                vol = float(np.std(returns))
                drawdown = abs(max_drawdown(returns))
                turnover = float(np.mean(turnovers)) if turnovers else 0.0
                score = mean - 0.35 * vol - 0.10 * drawdown / max(len(returns), 1)
                score -= 0.20 * turnover * (args.cost_bps / 10000.0)
                if weight > 0 and adapter_ic < proxy_ic - 0.01:
                    score -= weight * 0.0015
                if score > best_score:
                    best_score = score
                    best_weight = weight
        chosen_by_date[date] = best_weight

        for weight in weights:
            ret, turnover, symbols = candidate_metric(
                by_date[date], "base_z", "adapter_z", weight, previous[weight], topk, args.horizon, args.cost_bps
            )
            history[weight]["ret"].append(ret)
            history[weight]["turnover"].append(turnover)
            previous[weight] = symbols

        diagnostics.append(
            {
                "date": date,
                "topk": str(topk),
                "chosen_fintsb_weight": f"{best_weight:.6f}",
                "lagged_base_ic": f"{proxy_ic:.8f}",
                "lagged_fintsb_ic": f"{adapter_ic:.8f}",
                "history_days": str(max(0, min(args.gate_window, usable_end))),
            }
        )

    out_rows: list[dict] = []
    for date in dates:
        weight = chosen_by_date[date]
        for row in sorted(by_date[date], key=lambda item: str(item["symbol"])):
            score = (1.0 - weight) * float(row["base_z"]) + weight * float(row["adapter_z"])
            out_rows.append(clone_from(row, score))
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
    requested_topks = sorted(set(args.topk or [5, 10, 20, 30]), reverse=True)
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
        skipped_topks = sorted(set(requested_topks) - set(market_topks), reverse=True)
        if skipped_topks:
            print(f"{market} skipped_topk={skipped_topks} reason=universe_smaller_than_topk")

        lingxi = build_lingxi_scores(args, market, panel, stock_basic)
        runners = build_runner_scores(args, market, panel, stock_basic)
        lite = make_lite_scores(lingxi, runners["qlib_alpha158"], args.qlib_weight)
        base_methods = {
            "lingxi": lingxi,
            "qlib_alpha158": runners["qlib_alpha158"],
            "fintsb_ts": runners["fintsb_ts"],
            "lingxi_fusion_lite": lite,
        }
        for method, scored_rows in base_methods.items():
            for topk in market_topks:
                for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
                    row = summarize_daily(out_dir, market, method, topk, variant, score_field, scored_rows, args)
                    row["method_label"] = METHOD_LABELS[method]
                    summary_rows.append(row)
                    print(market, method, f"top{topk}", variant, row["ann_return"], row["sharpe"], row["mdd"])

        for topk in market_topks:
            regime = gate_scores(
                lingxi,
                runners["fintsb_ts"],
                topk,
                args,
                out_dir / market / f"lingxi_fusion_regime_h{args.horizon}_top{topk}_gate_diagnostics.csv",
            )
            full = gate_scores(
                lite,
                runners["fintsb_ts"],
                topk,
                args,
                out_dir / market / f"lingxi_fusion_full_h{args.horizon}_top{topk}_gate_diagnostics.csv",
            )
            for method, scored_rows in [("lingxi_fusion_regime", regime), ("lingxi_fusion_full", full)]:
                for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
                    row = summarize_daily(out_dir, market, method, topk, variant, score_field, scored_rows, args)
                    row["method_label"] = METHOD_LABELS[method]
                    summary_rows.append(row)
                    print(market, method, f"top{topk}", variant, row["ann_return"], row["sharpe"], row["mdd"])

    write_summary(out_dir / "lingxi_fusion_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'lingxi_fusion_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

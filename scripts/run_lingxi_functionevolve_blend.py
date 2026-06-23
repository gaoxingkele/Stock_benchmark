"""Blend Lingxi scores with promoted FunctionEvolve-style AST proxy factors."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from run_trade_validation import (  # noqa: E402
    backtest,
    fit_predictions,
    performance_stats,
    read_industry,
    read_meta,
    residualize_scores,
    write_daily,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data/processed/cn_a_share/csi300_2018_2024/panel.csv"))
    parser.add_argument("--stock-basic", default=str(PROJECT_ROOT / "data/raw/tushare/csi300_2018_2024/stock_basic.csv"))
    parser.add_argument("--proxy-detail", default=str(PROJECT_ROOT / "experiments/wq_functionevolve_proxy/functionevolve_proxy_detail.csv"))
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--lookback", type=int, default=20)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--valid-start", default="2022-01-04")
    parser.add_argument("--valid-end", default="2022-12-30")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2024-12-31")
    parser.add_argument("--ridge-alpha", type=float, default=10.0)
    parser.add_argument("--max-train-rows", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--blend-weight", action="append", type=float)
    parser.add_argument("--max-symbols", type=int, default=80)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_functionevolve_blend"))
    return parser.parse_args()


def to_float(value: str | float | int | None) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def safe_zscores(values: list[float]) -> list[float]:
    clean = [value for value in values if math.isfinite(value)]
    if len(clean) < 2:
        return [0.0 for _value in values]
    avg = mean(clean)
    std = pstdev(clean)
    if std == 0:
        return [0.0 for _value in values]
    return [(value - avg) / std if math.isfinite(value) else 0.0 for value in values]


def promoted_proxy_factors(path: Path) -> list[str]:
    factors: list[str] = []
    with path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if row["promotion_status"] == "promoted":
                factors.append(row["factor"])
    if not factors:
        raise ValueError("no promoted proxy factors found")
    return factors


def filtered_panel(source: Path, out_dir: Path, max_symbols: int) -> Path:
    if max_symbols <= 0:
        return source
    with source.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    symbols = sorted({row["symbol"] for row in rows})[:max_symbols]
    selected = {symbol for symbol in symbols}
    out_path = out_dir / f"panel_max_symbols_{max_symbols}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([row for row in rows if row["symbol"] in selected])
    return out_path


def proxy_zscore10_ret5_close(panel_path: Path) -> dict[tuple[str, str], float]:
    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with panel_path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            rows_by_symbol[row["symbol"]].append(row)

    raw_values: dict[tuple[str, str], float] = {}
    for symbol, rows in rows_by_symbol.items():
        rows = sorted(rows, key=lambda row: row["date"])
        closes = [to_float(row["close"]) for row in rows]
        ret5: list[float] = []
        for i, close in enumerate(closes):
            prev = closes[i - 5] if i >= 5 else float("nan")
            ret5.append(close / prev - 1.0 if close > 0 and prev > 0 else float("nan"))
        for i, row in enumerate(rows):
            window = [value for value in ret5[max(0, i - 9) : i + 1] if math.isfinite(value)]
            if len(window) < 2:
                value = float("nan")
            else:
                std = pstdev(window)
                value = (ret5[i] - mean(window)) / std if std and math.isfinite(ret5[i]) else float("nan")
            raw_values[(row["date"], symbol)] = value

    by_date: dict[str, list[tuple[tuple[str, str], float]]] = defaultdict(list)
    for key, value in raw_values.items():
        by_date[key[0]].append((key, value))
    normalized: dict[tuple[str, str], float] = {}
    for pairs in by_date.values():
        zscores = safe_zscores([value for _key, value in pairs])
        for (key, _value), zscore in zip(pairs, zscores):
            normalized[key] = zscore
    return normalized


def add_neutral_scores(scored_rows: list[dict], score_field: str, out_field: str) -> None:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in scored_rows:
        row["score"] = row[score_field]
        by_date[row["date"]].append(row)
    for rows in by_date.values():
        residuals = residualize_scores(rows)
        for row, residual in zip(rows, residuals):
            row[out_field] = float(residual)


def summarize(
    out_dir: Path,
    method: str,
    variant: str,
    score_field: str,
    topk: int,
    scored_rows: list[dict],
    args: argparse.Namespace,
) -> dict[str, str]:
    daily = backtest(scored_rows, score_field, topk, args.horizon, args.cost_bps)
    daily_path = out_dir / f"{method}_h{args.horizon}_top{topk}_{variant}_daily.csv"
    write_daily(daily_path, daily)
    stats = performance_stats(daily, "net_return")
    active_stats = performance_stats(daily, "net_active_return")
    return {
        "market": "cn_a_share",
        "method": method,
        "variant": variant,
        "horizon": str(args.horizon),
        "topk": str(topk),
        "cost_bps": f"{args.cost_bps:.2f}",
        "days": str(len(daily)),
        "ann_return": f"{stats['ann_return']:.8f}",
        "ann_vol": f"{stats['ann_vol']:.8f}",
        "sharpe": f"{stats['sharpe']:.8f}",
        "mdd": f"{stats['mdd']:.8f}",
        "cum_return": f"{stats['cum_return']:.8f}",
        "active_ann_return": f"{active_stats['ann_return']:.8f}",
        "active_sharpe": f"{active_stats['sharpe']:.8f}",
        "avg_turnover": f"{stats['avg_turnover']:.8f}",
        "hit_rate": f"{stats['hit_rate']:.8f}",
        "daily_source": str(daily_path.relative_to(PROJECT_ROOT)),
    }


def main() -> int:
    args = parse_args()
    topks = sorted(set(args.topk or [5, 10]))
    weights = sorted(set(args.blend_weight or [0.15, 0.30]))
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir
    panel_path = filtered_panel(Path(args.panel), out_dir, args.max_symbols)

    promoted = promoted_proxy_factors(Path(args.proxy_detail))
    if promoted != ["zscore10(ret5(close))"]:
        raise ValueError(f"unsupported promoted proxy factors for this smoke ablation: {promoted}")

    local_args = argparse.Namespace(**vars(args))
    local_args.panel = str(panel_path)
    local_args.model = ["rd_agent_quant"]
    rows, preds = fit_predictions(local_args, "rd_agent_quant")
    meta = read_meta(panel_path, read_industry(Path(args.stock_basic)))
    proxy_scores = proxy_zscore10_ret5_close(panel_path)

    scored_rows: list[dict] = []
    for row, pred in zip(rows, preds):
        row_meta = meta.get((row["date"], row["symbol"]), {})
        scored_rows.append(
            {
                "date": row["date"],
                "symbol": row["symbol"],
                "lingxi_score": float(pred),
                "proxy_score": proxy_scores.get((row["date"], row["symbol"]), 0.0),
                "label": float(row["label"]),
                "industry": row_meta.get("industry", "UNKNOWN"),
                "total_mv": float(row_meta.get("total_mv", float("nan"))),
            }
        )

    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in scored_rows:
        by_date[row["date"]].append(row)
    for rows_for_date in by_date.values():
        lingxi_z = safe_zscores([row["lingxi_score"] for row in rows_for_date])
        proxy_z = safe_zscores([row["proxy_score"] for row in rows_for_date])
        for row, lz, pz in zip(rows_for_date, lingxi_z, proxy_z):
            row["lingxi_raw"] = lz
            row["proxy_raw"] = pz
            for weight in weights:
                row[f"blend_w{weight:.2f}"] = (1.0 - weight) * lz + weight * pz

    add_neutral_scores(scored_rows, "lingxi_raw", "lingxi_neutral")
    for weight in weights:
        add_neutral_scores(scored_rows, f"blend_w{weight:.2f}", f"blend_w{weight:.2f}_neutral")

    summary_rows: list[dict[str, str]] = []
    for topk in topks:
        for variant, field in [("raw", "lingxi_raw"), ("industry_size_neutral", "lingxi_neutral")]:
            summary_rows.append(summarize(out_dir, "lingxi", variant, field, topk, scored_rows, args))
        for weight in weights:
            method = f"lingxi_functionevolve_memory_w{weight:.2f}"
            summary_rows.append(summarize(out_dir, method, "raw", f"blend_w{weight:.2f}", topk, scored_rows, args))
            summary_rows.append(
                summarize(out_dir, method, "industry_size_neutral", f"blend_w{weight:.2f}_neutral", topk, scored_rows, args)
            )

    fields = list(summary_rows[0])
    summary_path = out_dir / "lingxi_functionevolve_blend_summary.csv"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"summary={summary_path} rows={len(summary_rows)} promoted_proxy={promoted[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

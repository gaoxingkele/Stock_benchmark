"""Create explicit regime-gated AgentAdapt scores.

This gate extends the lagged performance gate with observable market and
portfolio-state features: CSI300 trend/volatility/drawdown, lagged alpha IC,
portfolio drawdown, turnover, industry concentration, and size exposure.
For H-day labels, decisions at date t use only dates up to t-H.
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

from run_score_trade_validation import load_label_lookup  # noqa: E402
from run_trade_validation import read_industry, read_meta  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proxy", required=True)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--panel", required=True)
    parser.add_argument("--stock-basic", required=True)
    parser.add_argument("--index-daily", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--diagnostics-out", required=True)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--topk", type=int, default=30)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--min-history", type=int, default=20)
    parser.add_argument("--weights", default="0,0.1,0.25,0.4")
    parser.add_argument("--default-weight", type=float, default=0.0)
    return parser.parse_args()


def to_float(value: str | None) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def read_scores(path: Path) -> dict[tuple[str, str], dict[str, float]]:
    rows = {}
    with path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            score = to_float(row.get("score"))
            label = to_float(row.get("label"))
            if math.isfinite(score) and math.isfinite(label):
                rows[(row["date"], row["symbol"])] = {"score": score, "label": label}
    return rows


def read_index_returns(path: Path) -> dict[str, float]:
    out: dict[str, float] = {}
    with path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            trade_date = row["trade_date"]
            date = f"{trade_date[:4]}-{trade_date[4:6]}-{trade_date[6:]}"
            close = to_float(row.get("close"))
            pre_close = to_float(row.get("pre_close"))
            if close > 0 and pre_close > 0:
                out[date] = close / pre_close - 1.0
    return out


def daily_z(values: dict[tuple[str, str], float]) -> dict[tuple[str, str], float]:
    by_date: dict[str, list[tuple[tuple[str, str], float]]] = defaultdict(list)
    for key, value in values.items():
        by_date[key[0]].append((key, value))
    out: dict[tuple[str, str], float] = {}
    for pairs in by_date.values():
        arr = np.asarray([value for _, value in pairs], dtype=float)
        mean = float(np.mean(arr))
        std = float(np.std(arr))
        if std <= 1e-12:
            std = 1.0
        for key, value in pairs:
            out[key] = (value - mean) / std
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


def corr(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 3:
        return 0.0
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    if float(np.std(x)) <= 1e-12 or float(np.std(y)) <= 1e-12:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def safe_mean(values: list[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def safe_std(values: list[float]) -> float:
    return float(np.std(values)) if values else 0.0


def portfolio_metric(
    rows: list[dict[str, float | str]],
    weight: float,
    previous: set[str],
    topk: int,
    horizon: int,
    cost_bps: float,
) -> dict[str, float | set[str]]:
    ranked = sorted(rows, key=lambda row: (1.0 - weight) * float(row["proxy_z"]) + weight * float(row["adapter_z"]), reverse=True)
    selected = ranked[:topk]
    if len(selected) < topk:
        return {"net_return": 0.0, "turnover": 0.0, "max_industry_weight": 0.0, "size_exposure": 0.0, "symbols": previous}
    symbols = {str(row["symbol"]) for row in selected}
    turnover = 0.5 * (len(symbols - previous) + len(previous - symbols)) / topk if previous else 0.5
    gross = float(np.mean([float(row["label"]) for row in selected]) / horizon)
    industry_weights: dict[str, float] = defaultdict(float)
    selected_size, universe_size = [], []
    for row in selected:
        industry_weights[str(row["industry"])] += 1.0 / topk
        if math.isfinite(float(row["total_mv"])):
            selected_size.append(math.log(max(float(row["total_mv"]), 1.0)))
    for row in rows:
        if math.isfinite(float(row["total_mv"])):
            universe_size.append(math.log(max(float(row["total_mv"]), 1.0)))
    size_exposure = float(np.mean(selected_size) - np.mean(universe_size)) if selected_size and universe_size else 0.0
    return {
        "net_return": gross - turnover * (cost_bps / 10000.0),
        "turnover": turnover,
        "max_industry_weight": max(industry_weights.values()) if industry_weights else 0.0,
        "size_exposure": size_exposure,
        "symbols": symbols,
    }


def score_candidate(
    weight: float,
    returns: list[float],
    turnovers: list[float],
    concentrations: list[float],
    size_exposures: list[float],
    proxy_returns: list[float],
    market_returns: list[float],
    proxy_ic: float,
    adapter_ic: float,
) -> tuple[float, str]:
    mean = float(np.mean(returns))
    vol = float(np.std(returns))
    drawdown = abs(max_drawdown(returns))
    turnover = float(np.mean(turnovers))
    concentration = float(np.mean(concentrations))
    size_abs = float(np.mean([abs(value) for value in size_exposures]))
    proxy_drawdown = abs(max_drawdown(proxy_returns))
    market_vol = float(np.std(market_returns)) if market_returns else 0.0
    market_trend = float(np.mean(market_returns)) if market_returns else 0.0
    market_drawdown = abs(max_drawdown(market_returns)) if market_returns else 0.0

    score = mean - 0.30 * vol - 0.12 * drawdown - 0.20 * turnover * 0.001 - 0.0006 * concentration - 0.0004 * size_abs
    reason = "base"
    if weight > 0:
        if adapter_ic < proxy_ic - 0.01:
            score -= weight * 0.0015
            reason = "adapter_ic_weak"
        if drawdown < proxy_drawdown and (market_vol > 0.012 or market_drawdown > 0.04 or market_trend < -0.001):
            score += weight * 0.0010
            reason = "risk_regime_adapter_helped"
        if concentration > 0.25 or size_abs > 0.35:
            score -= weight * 0.0008
            reason = "exposure_penalty"
    return score, reason


def main() -> int:
    args = parse_args()
    candidates = sorted({float(item.strip()) for item in args.weights.split(",") if item.strip()} | {args.default_weight})
    proxy = read_scores(Path(args.proxy))
    adapter = read_scores(Path(args.adapter))
    keys = sorted(set(proxy) & set(adapter))
    if not keys:
        raise RuntimeError("no overlapping proxy/adapter rows")

    meta = read_meta(Path(args.panel), read_industry(Path(args.stock_basic)))
    labels = load_label_lookup(Path(args.panel), args.horizon)
    proxy_z = daily_z({key: proxy[key]["score"] for key in keys})
    adapter_z = daily_z({key: adapter[key]["score"] for key in keys})
    market_returns = read_index_returns(Path(args.index_daily))

    by_date: dict[str, list[dict[str, float | str]]] = defaultdict(list)
    for date, symbol in keys:
        row_meta = meta.get((date, symbol), {})
        by_date[date].append(
            {
                "date": date,
                "symbol": symbol,
                "proxy_z": proxy_z[(date, symbol)],
                "adapter_z": adapter_z[(date, symbol)],
                "label": labels.get((date, symbol), proxy[(date, symbol)]["label"]),
                "industry": row_meta.get("industry", "UNKNOWN"),
                "total_mv": float(row_meta.get("total_mv", float("nan"))),
            }
        )
    dates = sorted(by_date)

    history: dict[float, dict[str, list[float]]] = {
        weight: {"ret": [], "turnover": [], "concentration": [], "size": []} for weight in candidates
    }
    previous: dict[float, set[str]] = {weight: set() for weight in candidates}
    chosen_by_date: dict[str, float] = {}
    diagnostics: list[dict[str, str]] = []

    for idx, date in enumerate(dates):
        usable_end = idx - args.horizon
        best_weight = args.default_weight
        best_score = float("-inf")
        best_reason = "cold_start"
        proxy_ic = adapter_ic = 0.0
        if usable_end >= args.min_history:
            start = max(0, usable_end - args.window)
            lagged_rows = [row for past_date in dates[start:usable_end] for row in by_date[past_date]]
            labels_l = [float(row["label"]) for row in lagged_rows]
            proxy_ic = corr([float(row["proxy_z"]) for row in lagged_rows], labels_l)
            adapter_ic = corr([float(row["adapter_z"]) for row in lagged_rows], labels_l)
            mkt = [market_returns.get(past_date, 0.0) for past_date in dates[start:usable_end]]
            proxy_returns = history[0.0]["ret"][start:usable_end]
            for weight in candidates:
                returns = history[weight]["ret"][start:usable_end]
                if len(returns) < args.min_history:
                    continue
                score, reason = score_candidate(
                    weight,
                    returns,
                    history[weight]["turnover"][start:usable_end],
                    history[weight]["concentration"][start:usable_end],
                    history[weight]["size"][start:usable_end],
                    proxy_returns,
                    mkt,
                    proxy_ic,
                    adapter_ic,
                )
                if score > best_score:
                    best_weight = weight
                    best_score = score
                    best_reason = reason
        chosen_by_date[date] = best_weight

        for weight in candidates:
            metric = portfolio_metric(by_date[date], weight, previous[weight], args.topk, args.horizon, args.cost_bps)
            history[weight]["ret"].append(float(metric["net_return"]))
            history[weight]["turnover"].append(float(metric["turnover"]))
            history[weight]["concentration"].append(float(metric["max_industry_weight"]))
            history[weight]["size"].append(float(metric["size_exposure"]))
            previous[weight] = metric["symbols"]  # type: ignore[assignment]

        diagnostics.append(
            {
                "date": date,
                "chosen_adapter_weight": f"{best_weight:.6f}",
                "reason": best_reason,
                "lagged_proxy_ic": f"{proxy_ic:.8f}",
                "lagged_adapter_ic": f"{adapter_ic:.8f}",
                "market_ret_20": f"{safe_mean([market_returns.get(d, 0.0) for d in dates[max(0, idx - 20):idx]]):.8f}",
                "market_vol_20": f"{safe_std([market_returns.get(d, 0.0) for d in dates[max(0, idx - 20):idx]]):.8f}",
                "history_days": str(max(0, min(args.window, usable_end))),
            }
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "symbol", "score", "label", "adapter_weight"])
        writer.writeheader()
        for date in dates:
            weight = chosen_by_date[date]
            for row in sorted(by_date[date], key=lambda item: str(item["symbol"])):
                score = (1.0 - weight) * float(row["proxy_z"]) + weight * float(row["adapter_z"])
                writer.writerow(
                    {
                        "date": date,
                        "symbol": row["symbol"],
                        "score": f"{score:.10f}",
                        "label": f"{float(row['label']):.10f}",
                        "adapter_weight": f"{weight:.6f}",
                    }
                )

    diagnostics_out = Path(args.diagnostics_out)
    diagnostics_out.parent.mkdir(parents=True, exist_ok=True)
    with diagnostics_out.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(diagnostics[0]))
        writer.writeheader()
        writer.writerows(diagnostics)
    print(f"wrote {out} rows={sum(len(by_date[date]) for date in dates)} diagnostics={diagnostics_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Create Risk-Gated AgentAdapt scores from proxy and adapter score files.

The gate chooses the DoubleAdapt-core weight online from lagged validation
performance. For an H-day label, the gate at date t only uses outcomes at
least H trading dates behind t.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proxy", required=True, help="CSV with date,symbol,score,label.")
    parser.add_argument("--adapter", required=True, help="CSV with date,symbol,score,label.")
    parser.add_argument("--out", required=True)
    parser.add_argument("--diagnostics-out", required=True)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--topk", type=int, default=30)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--min-history", type=int, default=20)
    parser.add_argument("--risk-aversion", type=float, default=0.35)
    parser.add_argument("--turnover-penalty", type=float, default=0.20)
    parser.add_argument("--weights", default="0,0.1,0.25,0.4", help="Candidate adapter weights.")
    parser.add_argument("--default-weight", type=float, default=0.0)
    return parser.parse_args()


def to_float(value: str | None) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def read_scores(path: Path) -> dict[tuple[str, str], dict[str, float | str]]:
    rows: dict[tuple[str, str], dict[str, float | str]] = {}
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            score = to_float(row.get("score"))
            label = to_float(row.get("label"))
            if math.isfinite(score) and math.isfinite(label):
                rows[(row["date"], row["symbol"])] = {"score": score, "label": label}
    return rows


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
    sx = float(np.std(x))
    sy = float(np.std(y))
    if sx <= 1e-12 or sy <= 1e-12:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def select_top_return(
    rows: list[dict[str, float | str]],
    weight: float,
    previous: set[str],
    topk: int,
    horizon: int,
    cost_bps: float,
) -> tuple[float, set[str], float]:
    ranked = sorted(rows, key=lambda row: float(row["proxy_z"]) * (1.0 - weight) + float(row["adapter_z"]) * weight, reverse=True)
    selected = ranked[:topk]
    symbols = {str(row["symbol"]) for row in selected}
    if len(selected) < topk:
        return 0.0, previous, 0.0
    turnover = 0.5 * (len(symbols - previous) + len(previous - symbols)) / topk if previous else 0.5
    gross = float(np.mean([float(row["label"]) for row in selected]) / horizon)
    net = gross - turnover * (cost_bps / 10000.0)
    return net, symbols, turnover


def main() -> int:
    args = parse_args()
    candidates = [float(item.strip()) for item in args.weights.split(",") if item.strip()]
    if args.default_weight not in candidates:
        candidates = sorted(set(candidates + [args.default_weight]))

    proxy = read_scores(Path(args.proxy))
    adapter = read_scores(Path(args.adapter))
    keys = sorted(set(proxy) & set(adapter))
    if not keys:
        raise RuntimeError("no overlapping proxy/adapter score rows")
    proxy_z = daily_z({key: float(proxy[key]["score"]) for key in keys})
    adapter_z = daily_z({key: float(adapter[key]["score"]) for key in keys})

    by_date: dict[str, list[dict[str, float | str]]] = defaultdict(list)
    for date, symbol in keys:
        by_date[date].append(
            {
                "date": date,
                "symbol": symbol,
                "proxy_z": proxy_z[(date, symbol)],
                "adapter_z": adapter_z[(date, symbol)],
                "label": float(proxy[(date, symbol)]["label"]),
            }
        )
    dates = sorted(by_date)

    candidate_returns: dict[float, list[float]] = {weight: [] for weight in candidates}
    candidate_turnover: dict[float, list[float]] = {weight: [] for weight in candidates}
    candidate_previous: dict[float, set[str]] = {weight: set() for weight in candidates}
    chosen_by_date: dict[str, float] = {}
    diagnostics: list[dict[str, str]] = []

    for idx, date in enumerate(dates):
        usable_end = idx - args.horizon
        best_weight = args.default_weight
        best_score = float("-inf")
        proxy_ic = 0.0
        adapter_ic = 0.0
        if usable_end >= args.min_history:
            start = max(0, usable_end - args.window)
            for weight in candidates:
                returns = candidate_returns[weight][start:usable_end]
                turnovers = candidate_turnover[weight][start:usable_end]
                if len(returns) < args.min_history:
                    continue
                mean = float(np.mean(returns))
                vol = float(np.std(returns))
                drawdown = abs(max_drawdown(returns))
                turnover = float(np.mean(turnovers)) if turnovers else 0.0
                score = mean - args.risk_aversion * vol - args.turnover_penalty * turnover * (args.cost_bps / 10000.0) - 0.10 * drawdown / max(len(returns), 1)
                if score > best_score:
                    best_score = score
                    best_weight = weight
            lagged_rows = [row for past_date in dates[start:usable_end] for row in by_date[past_date]]
            proxy_ic = corr([float(row["proxy_z"]) for row in lagged_rows], [float(row["label"]) for row in lagged_rows])
            adapter_ic = corr([float(row["adapter_z"]) for row in lagged_rows], [float(row["label"]) for row in lagged_rows])
        chosen_by_date[date] = best_weight

        for weight in candidates:
            ret, symbols, turnover = select_top_return(
                by_date[date], weight, candidate_previous[weight], args.topk, args.horizon, args.cost_bps
            )
            candidate_returns[weight].append(ret)
            candidate_turnover[weight].append(turnover)
            candidate_previous[weight] = symbols

        diagnostics.append(
            {
                "date": date,
                "chosen_adapter_weight": f"{best_weight:.6f}",
                "lagged_proxy_ic": f"{proxy_ic:.8f}",
                "lagged_adapter_ic": f"{adapter_ic:.8f}",
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
        writer = csv.DictWriter(file, fieldnames=["date", "chosen_adapter_weight", "lagged_proxy_ic", "lagged_adapter_ic", "history_days"])
        writer.writeheader()
        writer.writerows(diagnostics)
    print(f"wrote {out} rows={sum(len(by_date[date]) for date in dates)} diagnostics={diagnostics_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

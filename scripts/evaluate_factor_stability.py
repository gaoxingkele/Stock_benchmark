"""Evaluate factor IC decay and top-quantile turnover."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import safe_ir, safe_mean, spearman_corr  # noqa: E402


ID_FIELDS = {"date", "symbol", "ts_code"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_by_date_smoke" / "panel.csv"))
    parser.add_argument("--factors", default=str(PROJECT_ROOT / "data" / "features" / "basic_factors" / "csi300_by_date_smoke.csv"))
    parser.add_argument("--horizons", default="1,2,3,5", help="Comma-separated forward return horizons.")
    parser.add_argument("--top-frac", type=float, default=0.2, help="Top quantile fraction for turnover.")
    parser.add_argument("--decay-out", default=str(PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_decay_csi300_by_date.csv"))
    parser.add_argument("--turnover-out", default=str(PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_turnover_csi300_by_date.csv"))
    return parser.parse_args()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def build_labels(panel_path: Path, horizons: list[int]) -> dict[int, dict[tuple[str, str], float]]:
    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with panel_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows_by_symbol[row["symbol"]].append(row)

    labels_by_horizon: dict[int, dict[tuple[str, str], float]] = {horizon: {} for horizon in horizons}
    for symbol, rows in rows_by_symbol.items():
        rows = sorted(rows, key=lambda row: row["date"])
        for i, row in enumerate(rows):
            close = to_float(row["close"])
            if close <= 0 or math.isnan(close):
                continue
            for horizon in horizons:
                j = i + horizon
                if j >= len(rows):
                    continue
                future_close = to_float(rows[j]["close"])
                if not math.isnan(future_close):
                    labels_by_horizon[horizon][(row["date"], symbol)] = future_close / close - 1.0
    return labels_by_horizon


def read_factor_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        factor_names = [name for name in fieldnames if name not in ID_FIELDS]
        return factor_names, list(reader)


def compute_decay(
    factor_names: list[str],
    factor_rows: list[dict[str, str]],
    labels_by_horizon: dict[int, dict[tuple[str, str], float]],
) -> list[dict[str, str]]:
    out_rows: list[dict[str, str]] = []
    for horizon, labels in sorted(labels_by_horizon.items()):
        by_factor_date: dict[str, dict[str, list[tuple[float, float]]]] = defaultdict(lambda: defaultdict(list))
        for row in factor_rows:
            key = (row["date"], row["symbol"])
            if key not in labels:
                continue
            label = labels[key]
            for factor in factor_names:
                value = to_float(row.get(factor, ""))
                if not math.isnan(value):
                    by_factor_date[factor][row["date"]].append((value, label))

        for factor in sorted(by_factor_date):
            rankic_values: list[float] = []
            n_total = 0
            for date in sorted(by_factor_date[factor]):
                pairs = by_factor_date[factor][date]
                if len(pairs) < 2:
                    continue
                rankic_values.append(spearman_corr([score for score, _ in pairs], [label for _, label in pairs]))
                n_total += len(pairs)
            out_rows.append(
                {
                    "factor": factor,
                    "horizon": str(horizon),
                    "n": str(n_total),
                    "dates": str(len(rankic_values)),
                    "rankic": f"{safe_mean(rankic_values):.8f}",
                    "rankicir": f"{safe_ir(rankic_values):.8f}",
                }
            )
    out_rows.sort(key=lambda row: (row["factor"], int(row["horizon"])))
    return out_rows


def top_symbols(rows: list[dict[str, str]], factor: str, top_frac: float) -> set[str]:
    scored = [(to_float(row.get(factor, "")), row["symbol"]) for row in rows]
    scored = [(score, symbol) for score, symbol in scored if not math.isnan(score)]
    if not scored:
        return set()
    scored.sort(key=lambda item: item[0], reverse=True)
    top_n = max(1, math.ceil(len(scored) * top_frac))
    return {symbol for _, symbol in scored[:top_n]}


def compute_turnover(factor_names: list[str], factor_rows: list[dict[str, str]], top_frac: float) -> list[dict[str, str]]:
    rows_by_date: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in factor_rows:
        rows_by_date[row["date"]].append(row)
    dates = sorted(rows_by_date)

    out_rows: list[dict[str, str]] = []
    for factor in sorted(factor_names):
        daily_turnover: list[float] = []
        prev: set[str] | None = None
        avg_top_size_values: list[int] = []
        for date in dates:
            current = top_symbols(rows_by_date[date], factor, top_frac)
            if not current:
                continue
            avg_top_size_values.append(len(current))
            if prev:
                denominator = min(len(prev), len(current))
                if denominator > 0:
                    daily_turnover.append(1.0 - len(prev & current) / denominator)
            prev = current
        out_rows.append(
            {
                "factor": factor,
                "top_frac": f"{top_frac:.4f}",
                "dates": str(len(avg_top_size_values)),
                "turnover_obs": str(len(daily_turnover)),
                "avg_top_size": f"{safe_mean([float(v) for v in avg_top_size_values]):.2f}",
                "avg_turnover": f"{safe_mean(daily_turnover):.8f}",
            }
        )
    out_rows.sort(key=lambda row: float(row["avg_turnover"]) if row["avg_turnover"] != "nan" else 999)
    return out_rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    horizons = [int(item.strip()) for item in args.horizons.split(",") if item.strip()]
    if not horizons:
        raise RuntimeError("at least one horizon is required")
    if not 0 < args.top_frac <= 1:
        raise RuntimeError("--top-frac must be in (0, 1]")

    factor_names, factor_rows = read_factor_rows(Path(args.factors))
    labels_by_horizon = build_labels(Path(args.panel), horizons)
    decay_rows = compute_decay(factor_names, factor_rows, labels_by_horizon)
    turnover_rows = compute_turnover(factor_names, factor_rows, args.top_frac)

    write_csv(Path(args.decay_out), decay_rows, ["factor", "horizon", "n", "dates", "rankic", "rankicir"])
    write_csv(Path(args.turnover_out), turnover_rows, ["factor", "top_frac", "dates", "turnover_obs", "avg_top_size", "avg_turnover"])

    print(f"decay={args.decay_out} rows={len(decay_rows)}")
    print(f"turnover={args.turnover_out} rows={len(turnover_rows)}")
    for row in sorted(decay_rows, key=lambda item: abs(float(item["rankic"])) if item["rankic"] != "nan" else -1, reverse=True)[:5]:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Generate Qlib-style Alpha158/Alpha360 compatible factor CSV files.

The current environment cannot run Qlib's expression engine, so this script
creates deterministic CSV features with the same benchmark-facing contract:
`date,symbol,ts_code` plus numeric factor columns that can be validated by the
shared factor IC tooling.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WINDOWS_158 = [5, 10, 20, 30, 60]
WINDOWS_360 = [2, 3, 5, 10, 20, 30, 60]
BASE_FIELDS = [
    "open",
    "high",
    "low",
    "close",
    "pre_close",
    "volume",
    "amount",
    "turnover_rate",
    "volume_ratio",
    "pe",
    "pb",
    "total_mv",
    "circ_mv",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_2018_2024" / "panel.csv"))
    parser.add_argument("--kind", choices=["alpha158", "alpha360"], required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def safe_div(left: float, right: float) -> float:
    if right == 0 or math.isnan(left) or math.isnan(right):
        return float("nan")
    return left / right


def safe_log(value: float) -> float:
    return math.log(value) if value > 0 and not math.isnan(value) else float("nan")


def clean(values: list[float]) -> list[float]:
    return [value for value in values if not math.isnan(value)]


def mean(values: list[float]) -> float:
    items = clean(values)
    return sum(items) / len(items) if items else float("nan")


def std(values: list[float]) -> float:
    items = clean(values)
    if len(items) < 2:
        return float("nan")
    avg = sum(items) / len(items)
    return math.sqrt(sum((value - avg) ** 2 for value in items) / len(items))


def minimum(values: list[float]) -> float:
    items = clean(values)
    return min(items) if items else float("nan")


def maximum(values: list[float]) -> float:
    items = clean(values)
    return max(items) if items else float("nan")


def corr(left: list[float], right: list[float]) -> float:
    pairs = [(x, y) for x, y in zip(left, right) if not math.isnan(x) and not math.isnan(y)]
    if len(pairs) < 2:
        return float("nan")
    xs = [x for x, _ in pairs]
    ys = [y for _, y in pairs]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    dx = [x - mx for x in xs]
    dy = [y - my for y in ys]
    denom = math.sqrt(sum(x * x for x in dx) * sum(y * y for y in dy))
    if denom == 0:
        return float("nan")
    return sum(x * y for x, y in zip(dx, dy)) / denom


def fmt(value: float) -> str:
    return "" if math.isnan(value) or math.isinf(value) else f"{value:.10f}"


def load_panel(path: Path) -> dict[str, list[dict[str, str]]]:
    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows_by_symbol[row["symbol"]].append(row)
    for rows in rows_by_symbol.values():
        rows.sort(key=lambda item: item["date"])
    return dict(rows_by_symbol)


def rolling(values: list[float], idx: int, window: int) -> list[float]:
    return values[max(0, idx - window + 1) : idx + 1]


def add_price_volume_features(features: dict[str, float], series: dict[str, list[float]], idx: int, windows: list[int]) -> None:
    close = series["close"][idx]
    open_ = series["open"][idx]
    high = series["high"][idx]
    low = series["low"][idx]
    volume = series["volume"][idx]
    amount = series["amount"][idx]
    pre_close = series["pre_close"][idx]

    features.update(
        {
            "kmid": safe_div(close, open_) - 1,
            "klen": safe_div(high, low) - 1,
            "kmid2": safe_div(close - open_, high - low),
            "kup": safe_div(high - max(open_, close), open_),
            "klow": safe_div(min(open_, close) - low, open_),
            "ksft": safe_div((close - open_) * 2, high - low),
            "gap": safe_div(open_, pre_close) - 1,
            "log_volume": safe_log(volume),
            "log_amount": safe_log(amount),
            "log_total_mv": safe_log(series["total_mv"][idx]),
            "log_circ_mv": safe_log(series["circ_mv"][idx]),
            "pe": series["pe"][idx],
            "pb": series["pb"][idx],
            "turnover_rate": series["turnover_rate"][idx],
            "volume_ratio": series["volume_ratio"][idx],
        }
    )

    returns = [safe_div(series["close"][j], series["close"][j - 1]) - 1 if j > 0 else float("nan") for j in range(len(series["close"]))]
    for window in windows:
        close_w = rolling(series["close"], idx, window)
        high_w = rolling(series["high"], idx, window)
        low_w = rolling(series["low"], idx, window)
        volume_w = rolling(series["volume"], idx, window)
        amount_w = rolling(series["amount"], idx, window)
        ret_w = rolling(returns, idx, window)

        prev_idx = idx - window
        prev_close = series["close"][prev_idx] if prev_idx >= 0 else float("nan")
        features[f"roc_{window}"] = safe_div(close, prev_close) - 1
        features[f"ma_ratio_{window}"] = safe_div(close, mean(close_w)) - 1
        features[f"std_ret_{window}"] = std(ret_w)
        features[f"max_ret_{window}"] = maximum(ret_w)
        features[f"min_ret_{window}"] = minimum(ret_w)
        features[f"high_ratio_{window}"] = safe_div(close, maximum(high_w)) - 1
        features[f"low_ratio_{window}"] = safe_div(close, minimum(low_w)) - 1
        features[f"volume_ma_ratio_{window}"] = safe_div(volume, mean(volume_w)) - 1
        features[f"amount_ma_ratio_{window}"] = safe_div(amount, mean(amount_w)) - 1
        features[f"volume_std_{window}"] = safe_div(std(volume_w), mean(volume_w))
        features[f"amount_std_{window}"] = safe_div(std(amount_w), mean(amount_w))
        features[f"pv_corr_{window}"] = corr(close_w, volume_w)
        features[f"pa_corr_{window}"] = corr(close_w, amount_w)


def add_alpha360_lag_features(features: dict[str, float], series: dict[str, list[float]], idx: int) -> None:
    close = series["close"][idx]
    volume = series["volume"][idx]
    amount = series["amount"][idx]
    for lag in range(1, 61):
        j = idx - lag
        if j < 0:
            features[f"close_lag_ratio_{lag}"] = float("nan")
            features[f"volume_lag_ratio_{lag}"] = float("nan")
            features[f"amount_lag_ratio_{lag}"] = float("nan")
        else:
            features[f"close_lag_ratio_{lag}"] = safe_div(close, series["close"][j]) - 1
            features[f"volume_lag_ratio_{lag}"] = safe_div(volume, series["volume"][j]) - 1
            features[f"amount_lag_ratio_{lag}"] = safe_div(amount, series["amount"][j]) - 1


def main() -> int:
    args = parse_args()
    rows_by_symbol = load_panel(Path(args.panel))
    windows = WINDOWS_158 if args.kind == "alpha158" else WINDOWS_360
    out_rows: list[dict[str, str]] = []
    factor_names: list[str] | None = None

    for symbol, rows in rows_by_symbol.items():
        series = {field: [to_float(row[field]) for row in rows] for field in BASE_FIELDS}
        for idx, row in enumerate(rows):
            features: dict[str, float] = {}
            add_price_volume_features(features, series, idx, windows)
            if args.kind == "alpha360":
                add_alpha360_lag_features(features, series, idx)
            if factor_names is None:
                factor_names = list(features.keys())
            out = {"date": row["date"], "symbol": symbol, "ts_code": row["ts_code"]}
            for name in factor_names:
                out[name] = fmt(features.get(name, float("nan")))
            out_rows.append(out)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    names = factor_names or []
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "symbol", "ts_code"] + names)
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"features={out_path} rows={len(out_rows)} symbols={len(rows_by_symbol)} feature_count={len(names)} kind={args.kind}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

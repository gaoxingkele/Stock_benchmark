"""Generate a small library of basic price-volume factors from panel.csv."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_by_date_smoke" / "panel.csv"))
    parser.add_argument("--out", default=str(PROJECT_ROOT / "data" / "features" / "basic_factors" / "csi300_by_date_smoke.csv"))
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


def rolling_mean(values: list[float]) -> float:
    clean = [v for v in values if not math.isnan(v)]
    if not clean:
        return float("nan")
    return sum(clean) / len(clean)


def main() -> int:
    args = parse_args()
    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with Path(args.panel).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows_by_symbol[row["symbol"]].append(row)

    out_rows: list[dict[str, str]] = []
    for symbol, rows in rows_by_symbol.items():
        rows = sorted(rows, key=lambda row: row["date"])
        closes = [to_float(row["close"]) for row in rows]
        volumes = [to_float(row["volume"]) for row in rows]
        amounts = [to_float(row["amount"]) for row in rows]
        for i, row in enumerate(rows):
            close = closes[i]
            open_ = to_float(row["open"])
            high = to_float(row["high"])
            low = to_float(row["low"])
            volume = volumes[i]
            amount = amounts[i]
            pre_close = to_float(row["pre_close"])
            prev_close = closes[i - 1] if i >= 1 else float("nan")
            prev3_close = closes[i - 3] if i >= 3 else float("nan")
            vol_mean3 = rolling_mean(volumes[max(0, i - 2) : i + 1])
            amount_mean3 = rolling_mean(amounts[max(0, i - 2) : i + 1])

            factors = {
                "ret_1": safe_div(close, prev_close) - 1 if i >= 1 else float("nan"),
                "ret_3": safe_div(close, prev3_close) - 1 if i >= 3 else float("nan"),
                "intraday_ret": safe_div(close, open_) - 1,
                "overnight_ret": safe_div(open_, pre_close) - 1,
                "high_low_spread": safe_div(high, low) - 1,
                "close_to_high": safe_div(close, high),
                "close_to_low": safe_div(close, low),
                "volume_ratio_3": safe_div(volume, vol_mean3),
                "amount_ratio_3": safe_div(amount, amount_mean3),
                "turnover_rate": to_float(row["turnover_rate"]),
                "volume_ratio": to_float(row["volume_ratio"]),
                "pe": to_float(row["pe"]),
                "pb": to_float(row["pb"]),
                "size_log_total_mv": math.log(to_float(row["total_mv"])) if to_float(row["total_mv"]) > 0 else float("nan"),
                "size_log_circ_mv": math.log(to_float(row["circ_mv"])) if to_float(row["circ_mv"]) > 0 else float("nan"),
            }
            out = {"date": row["date"], "symbol": symbol, "ts_code": row["ts_code"]}
            for name, value in factors.items():
                out[name] = "" if math.isnan(value) else f"{value:.10f}"
            out_rows.append(out)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["date", "symbol", "ts_code"] + list(factors.keys())
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"factors={out_path} rows={len(out_rows)} symbols={len(rows_by_symbol)} factor_count={len(fieldnames) - 3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


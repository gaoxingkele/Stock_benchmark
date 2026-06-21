"""Build a processed China A-share panel and Qlib-friendly CSV files.

Input raw files are produced by `download_csi300_tushare.py`.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


PRICE_FIELDS = ["open", "high", "low", "close", "pre_close"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", default=str(PROJECT_ROOT / "data" / "raw" / "tushare" / "csi300"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300"))
    parser.add_argument("--adjust", choices=["none", "forward"], default="forward")
    parser.add_argument("--universe-only", action="store_true", help="Keep only stocks present in index_weight.csv.")
    return parser.parse_args()


def read_keyed_csv(path: Path, key_fields: tuple[str, ...]) -> dict[tuple[str, ...], dict[str, str]]:
    data: dict[tuple[str, ...], dict[str, str]] = {}
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = tuple(row[field] for field in key_fields)
            data[key] = row
    return data


def read_index_weights(path: Path) -> tuple[list[str], dict[str, tuple[str, str]]]:
    codes: list[str] = []
    seen: set[str] = set()
    ranges: dict[str, list[str]] = defaultdict(list)
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row["con_code"]
            date = format_date(row["trade_date"])
            if code not in seen:
                seen.add(code)
                codes.append(code)
            ranges[code].append(date)
    return codes, {code: (min(dates), max(dates)) for code, dates in ranges.items()}


def format_date(value: str) -> str:
    value = value.strip()
    if len(value) == 8 and value.isdigit():
        return f"{value[:4]}-{value[4:6]}-{value[6:]}"
    return value


def to_float(value: str, default: float = 0.0) -> float:
    try:
        if value == "" or value is None:
            return default
        return float(value)
    except ValueError:
        return default


def qlib_symbol(ts_code: str) -> str:
    code, exchange = ts_code.split(".")
    return f"{exchange.lower()}{code}"


def main() -> int:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    panel_path = out_dir / "panel.csv"
    qlib_csv_dir = out_dir / "qlib_csv"
    instrument_dir = out_dir / "instruments"
    calendar_dir = out_dir / "calendars"
    for path in [out_dir, qlib_csv_dir, instrument_dir, calendar_dir]:
        path.mkdir(parents=True, exist_ok=True)

    daily_basic = read_keyed_csv(raw_dir / "daily_basic.csv", ("ts_code", "trade_date"))
    adj_factor = read_keyed_csv(raw_dir / "adj_factor.csv", ("ts_code", "trade_date"))
    codes, ranges = read_index_weights(raw_dir / "index_weight.csv")
    code_set = set(codes)

    calendars: list[str] = []
    with (raw_dir / "trade_cal.csv").open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        calendars = sorted(format_date(row["cal_date"]) for row in reader if row.get("is_open") == "1")
    (calendar_dir / "day.txt").write_text("\n".join(calendars) + "\n", encoding="utf-8")

    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with (raw_dir / "daily.csv").open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ts_code = row["ts_code"]
            if args.universe_only and ts_code not in code_set:
                continue
            trade_date = row["trade_date"]
            basic = daily_basic.get((ts_code, trade_date), {})
            adj = adj_factor.get((ts_code, trade_date), {})
            adj_value = to_float(adj.get("adj_factor", "1"), 1.0)
            out = {
                "symbol": qlib_symbol(ts_code),
                "date": format_date(trade_date),
                "ts_code": ts_code,
                "volume": row.get("vol", ""),
                "amount": row.get("amount", ""),
                "change": row.get("change", ""),
                "pct_chg": row.get("pct_chg", ""),
                "turnover_rate": basic.get("turnover_rate", ""),
                "volume_ratio": basic.get("volume_ratio", ""),
                "pe": basic.get("pe", ""),
                "pb": basic.get("pb", ""),
                "total_mv": basic.get("total_mv", ""),
                "circ_mv": basic.get("circ_mv", ""),
                "factor": str(adj_value),
            }
            for field in PRICE_FIELDS:
                out[field] = row.get(field, "")
            rows_by_symbol[out["symbol"]].append(out)

    fieldnames = [
        "symbol",
        "date",
        "ts_code",
        "open",
        "high",
        "low",
        "close",
        "pre_close",
        "volume",
        "amount",
        "change",
        "pct_chg",
        "turnover_rate",
        "volume_ratio",
        "pe",
        "pb",
        "total_mv",
        "circ_mv",
        "factor",
    ]
    with panel_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for symbol in sorted(rows_by_symbol):
            rows = sorted(rows_by_symbol[symbol], key=lambda x: x["date"])
            if args.adjust == "forward" and rows:
                norm_factor = to_float(rows[-1].get("factor", "1"), 1.0)
                for row in rows:
                    row_factor = to_float(row.get("factor", "1"), 1.0)
                    scale = row_factor / norm_factor if norm_factor else 1.0
                    for field in PRICE_FIELDS:
                        row[field] = f"{to_float(row.get(field, '')) * scale:.6f}"
            writer.writerows(rows)
            with (qlib_csv_dir / f"{symbol}.csv").open("w", newline="", encoding="utf-8") as stock_file:
                stock_writer = csv.DictWriter(stock_file, fieldnames=fieldnames)
                stock_writer.writeheader()
                stock_writer.writerows(rows)

    all_lines = []
    csi300_lines = []
    for code in codes:
        symbol = qlib_symbol(code)
        if symbol in rows_by_symbol:
            dates = [row["date"] for row in rows_by_symbol[symbol]]
            start, end = min(dates), max(dates)
        else:
            start, end = ranges[code]
        line = f"{symbol}\t{start}\t{end}"
        all_lines.append(line)
        if symbol in rows_by_symbol:
            csi300_lines.append(line)
    (instrument_dir / "all.txt").write_text("\n".join(all_lines) + "\n", encoding="utf-8")
    (instrument_dir / "csi300.txt").write_text("\n".join(csi300_lines) + "\n", encoding="utf-8")

    print(f"panel={panel_path} rows={sum(len(v) for v in rows_by_symbol.values())} symbols={len(rows_by_symbol)}")
    print(f"qlib_csv_dir={qlib_csv_dir}")
    print(f"instruments={instrument_dir}")
    print(f"calendars={calendar_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

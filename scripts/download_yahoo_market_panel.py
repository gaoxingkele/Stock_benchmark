"""Download Yahoo Finance OHLCV data and build a benchmark panel.

The output panel uses the same columns as the China A-share experiments so the
existing paper-proxy and trading validation scripts can be reused.
"""

from __future__ import annotations

import argparse
import csv
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]


UNIVERSES = {
    "us_large_cap": [
        ("AAPL", "Technology"),
        ("MSFT", "Technology"),
        ("NVDA", "Technology"),
        ("AMZN", "Consumer Discretionary"),
        ("META", "Communication Services"),
        ("GOOGL", "Communication Services"),
        ("GOOG", "Communication Services"),
        ("BRK-B", "Financials"),
        ("LLY", "Health Care"),
        ("JPM", "Financials"),
        ("AVGO", "Technology"),
        ("XOM", "Energy"),
        ("UNH", "Health Care"),
        ("V", "Financials"),
        ("MA", "Financials"),
        ("COST", "Consumer Staples"),
        ("HD", "Consumer Discretionary"),
        ("PG", "Consumer Staples"),
        ("JNJ", "Health Care"),
        ("WMT", "Consumer Staples"),
        ("BAC", "Financials"),
        ("NFLX", "Communication Services"),
        ("CRM", "Technology"),
        ("AMD", "Technology"),
        ("KO", "Consumer Staples"),
        ("PEP", "Consumer Staples"),
        ("ADBE", "Technology"),
        ("ORCL", "Technology"),
        ("CSCO", "Technology"),
        ("INTC", "Technology"),
        ("PFE", "Health Care"),
        ("TMO", "Health Care"),
        ("MCD", "Consumer Discretionary"),
        ("DIS", "Communication Services"),
        ("ABT", "Health Care"),
        ("MRK", "Health Care"),
        ("NKE", "Consumer Discretionary"),
        ("IBM", "Technology"),
        ("GE", "Industrials"),
        ("CAT", "Industrials"),
    ],
    "hk_large_cap": [
        ("0700.HK", "Communication Services"),
        ("9988.HK", "Consumer Discretionary"),
        ("3690.HK", "Consumer Discretionary"),
        ("9618.HK", "Consumer Discretionary"),
        ("1810.HK", "Technology"),
        ("2318.HK", "Financials"),
        ("1299.HK", "Financials"),
        ("0005.HK", "Financials"),
        ("0939.HK", "Financials"),
        ("1398.HK", "Financials"),
        ("3988.HK", "Financials"),
        ("0883.HK", "Energy"),
        ("0857.HK", "Energy"),
        ("0386.HK", "Energy"),
        ("0941.HK", "Communication Services"),
        ("0762.HK", "Communication Services"),
        ("2628.HK", "Financials"),
        ("3968.HK", "Financials"),
        ("2388.HK", "Financials"),
        ("0011.HK", "Financials"),
        ("0002.HK", "Utilities"),
        ("0003.HK", "Utilities"),
        ("0006.HK", "Utilities"),
        ("1113.HK", "Real Estate"),
        ("0823.HK", "Real Estate"),
        ("1109.HK", "Real Estate"),
        ("2020.HK", "Consumer Discretionary"),
        ("2331.HK", "Consumer Discretionary"),
        ("0175.HK", "Consumer Discretionary"),
        ("1211.HK", "Consumer Discretionary"),
        ("0027.HK", "Consumer Discretionary"),
        ("0066.HK", "Industrials"),
        ("0669.HK", "Technology"),
        ("2269.HK", "Health Care"),
        ("1177.HK", "Health Care"),
        ("1093.HK", "Health Care"),
        ("2319.HK", "Consumer Staples"),
        ("0291.HK", "Consumer Staples"),
        ("1928.HK", "Consumer Discretionary"),
        ("2015.HK", "Consumer Discretionary"),
    ],
    "crypto_major": [
        ("BTC-USD", "Layer1"),
        ("ETH-USD", "Layer1"),
        ("BNB-USD", "Exchange"),
        ("SOL-USD", "Layer1"),
        ("XRP-USD", "Payments"),
        ("ADA-USD", "Layer1"),
        ("DOGE-USD", "Meme"),
        ("TRX-USD", "Layer1"),
        ("AVAX-USD", "Layer1"),
        ("LINK-USD", "Oracle"),
        ("DOT-USD", "Layer1"),
        ("MATIC-USD", "Layer2"),
        ("LTC-USD", "Payments"),
        ("BCH-USD", "Payments"),
        ("UNI-USD", "DeFi"),
        ("ATOM-USD", "Layer1"),
        ("ETC-USD", "Layer1"),
        ("XLM-USD", "Payments"),
        ("FIL-USD", "Storage"),
        ("AAVE-USD", "DeFi"),
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--universe", choices=sorted(UNIVERSES), required=True)
    parser.add_argument("--start", default="2018-01-01")
    parser.add_argument("--end", default="2026-06-21")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--sleep", type=float, default=0.15)
    parser.add_argument("--retries", type=int, default=3)
    return parser.parse_args()


def unix_time(date: str) -> int:
    return int(datetime.fromisoformat(date).replace(tzinfo=timezone.utc).timestamp())


def fetch_chart(symbol: str, start: str, end: str, retries: int = 3) -> list[dict[str, float | str]]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {
        "period1": str(unix_time(start)),
        "period2": str(unix_time(end)),
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            break
        except Exception as exc:  # noqa: BLE001 - market data downloads need to continue by symbol
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    else:
        print(f"skip {symbol}: {last_error}")
        return []
    payload = response.json()
    result = payload.get("chart", {}).get("result") or []
    if not result:
        return []
    item = result[0]
    timestamps = item.get("timestamp") or []
    quote = (item.get("indicators", {}).get("quote") or [{}])[0]
    adjclose = (item.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose") or []
    rows: list[dict[str, float | str]] = []
    previous_close = None
    for idx, ts in enumerate(timestamps):
        open_ = value_at(quote.get("open"), idx)
        high = value_at(quote.get("high"), idx)
        low = value_at(quote.get("low"), idx)
        close = value_at(adjclose, idx)
        raw_close = value_at(quote.get("close"), idx)
        volume = value_at(quote.get("volume"), idx, default=0.0)
        if close is None:
            close = raw_close
        if None in {open_, high, low, close} or close <= 0:
            continue
        date = datetime.fromtimestamp(int(ts), tz=timezone.utc).date().isoformat()
        pre_close = previous_close if previous_close and previous_close > 0 else close
        change = close - pre_close
        pct_chg = change / pre_close * 100.0 if pre_close else 0.0
        amount = float(volume or 0.0) * close
        turnover_rate = abs(float(pct_chg))
        volume_ratio = float(volume or 0.0) / 1_000_000.0
        rows.append(
            {
                "date": date,
                "open": float(open_),
                "high": float(high),
                "low": float(low),
                "close": float(close),
                "pre_close": float(pre_close),
                "volume": float(volume or 0.0),
                "amount": amount,
                "change": change,
                "pct_chg": pct_chg,
                "turnover_rate": turnover_rate,
                "volume_ratio": volume_ratio,
                "pe": 0.0,
                "pb": 0.0,
                "total_mv": amount,
                "circ_mv": amount,
                "factor": close / raw_close if raw_close else 1.0,
            }
        )
        previous_close = close
    return rows


def value_at(values, idx: int, default=None):
    if values is None or idx >= len(values):
        return default
    value = values[idx]
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def write_panel(out_dir: Path, universe: str, rows: list[dict[str, str | float]], metadata: list[dict[str, str]]) -> None:
    panel_path = out_dir / "panel.csv"
    stock_basic_path = out_dir / "stock_basic.csv"
    out_dir.mkdir(parents=True, exist_ok=True)
    fields = [
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
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: (str(row["date"]), str(row["symbol"]))))
    with stock_basic_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ts_code", "symbol", "name", "area", "industry", "market", "list_date"])
        writer.writeheader()
        writer.writerows(metadata)
    manifest = out_dir / "universe.txt"
    manifest.write_text("\n".join(f"{row['ts_code']},{row['industry']}" for row in metadata) + "\n", encoding="utf-8")
    print(f"wrote {panel_path} rows={len(rows)} universe={universe} metadata={stock_basic_path}")


def main() -> int:
    args = parse_args()
    all_rows: list[dict[str, str | float]] = []
    metadata: list[dict[str, str]] = []
    for symbol, industry in UNIVERSES[args.universe]:
        rows = fetch_chart(symbol, args.start, args.end, args.retries)
        if not rows:
            print(f"skip {symbol}: no rows")
            continue
        ts_code = symbol
        metadata.append(
            {
                "ts_code": ts_code,
                "symbol": symbol,
                "name": symbol,
                "area": args.universe,
                "industry": industry,
                "market": args.universe,
                "list_date": args.start.replace("-", ""),
            }
        )
        for row in rows:
            all_rows.append({"symbol": symbol, "ts_code": ts_code, **row})
        print(f"{symbol}: {len(rows)} rows")
        time.sleep(args.sleep)
    write_panel(Path(args.out_dir), args.universe, all_rows, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

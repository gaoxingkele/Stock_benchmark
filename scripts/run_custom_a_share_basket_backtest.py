"""Backtest a custom A-share basket from public daily data."""

from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SYMBOLS = [
    "600160.SH",
    "600549.SH",
    "688257.SH",
    "002171.SZ",
    "603588.SH",
    "600909.SH",
    "300475.SZ",
    "300566.SZ",
    "688525.SH",
    "600176.SH",
    "000100.SZ",
    "688498.SH",
    "600206.SH",
    "688766.SH",
    "301099.SZ",
    "300031.SZ",
    "600522.SH",
    "001696.SZ",
    "600458.SH",
    "601208.SH",
    "300726.SZ",
    "688233.SH",
    "301536.SZ",
    "688549.SH",
    "300976.SZ",
    "603225.SH",
    "600498.SH",
    "600459.SH",
    "601211.SH",
    "002842.SZ",
    "600392.SH",
    "300304.SZ",
    "605589.SH",
    "300666.SZ",
    "300014.SZ",
    "603271.SH",
    "600378.SH",
    "688809.SH",
    "688378.SH",
    "688002.SH",
    "603045.SH",
    "000725.SZ",
    "002297.SZ",
    "688388.SH",
    "002378.SZ",
    "920357.BJ",
    "300975.SZ",
    "920394.BJ",
    "688146.SH",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default="20250101")
    parser.add_argument("--end", default="20260624")
    parser.add_argument("--adjust", default="hfq", choices=["", "qfq", "hfq"])
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/custom_a_share_basket"))
    parser.add_argument("--sleep", type=float, default=0.2)
    return parser.parse_args()


def plain_symbol(ts_code: str) -> str:
    return ts_code.split(".")[0]


def load_akshare():
    try:
        import akshare as ak  # type: ignore
    except ImportError as exc:
        raise RuntimeError("akshare is required: python -m pip install akshare") from exc
    return ak


def fetch_one(ak, ts_code: str, start: str, end: str, adjust: str) -> pd.DataFrame:
    symbol = plain_symbol(ts_code)
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start, end_date=end, adjust=adjust)
    if df.empty:
        return pd.DataFrame(columns=["date", "ts_code", "close"])
    columns = {col: str(col) for col in df.columns}
    df = df.rename(columns=columns)
    date_col = "日期"
    close_col = "收盘"
    out = pd.DataFrame(
        {
            "date": pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d"),
            "ts_code": ts_code,
            "close": pd.to_numeric(df[close_col], errors="coerce"),
        }
    )
    return out.dropna(subset=["close"])


def tx_symbol(ts_code: str) -> str:
    code, exchange = ts_code.split(".")
    if exchange == "SH":
        return f"sh{code}"
    if exchange == "SZ":
        return f"sz{code}"
    if exchange == "BJ":
        return f"bj{code}"
    return code


def fetch_one_tx(ak, ts_code: str, start: str, end: str, adjust: str) -> pd.DataFrame:
    df = ak.stock_zh_a_hist_tx(symbol=tx_symbol(ts_code), start_date=start, end_date=end, adjust=adjust)
    if df.empty:
        return pd.DataFrame(columns=["date", "ts_code", "close"])
    out = pd.DataFrame(
        {
            "date": pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d"),
            "ts_code": ts_code,
            "close": pd.to_numeric(df["close"], errors="coerce"),
        }
    )
    return out.dropna(subset=["close"])


def max_drawdown(values: list[float]) -> float:
    nav = 1.0
    peak = 1.0
    worst = 0.0
    for value in values:
        nav *= 1.0 + value
        peak = max(peak, nav)
        worst = min(worst, nav / peak - 1.0)
    return worst


def stats(daily: pd.DataFrame) -> dict[str, float]:
    if daily.empty or "net_return" not in daily:
        return {key: float("nan") for key in ["days", "ann_return", "ann_vol", "sharpe", "mdd", "cum_return", "avg_turnover", "hit_rate"]}
    returns = daily["net_return"].astype(float).tolist()
    if not returns:
        return {key: float("nan") for key in ["days", "ann_return", "ann_vol", "sharpe", "mdd", "cum_return", "avg_turnover", "hit_rate"]}
    nav = float(np.prod([1.0 + value for value in returns]))
    ann_return = nav ** (252.0 / len(returns)) - 1.0
    ann_vol = float(np.std(returns) * math.sqrt(252.0))
    return {
        "days": float(len(returns)),
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "sharpe": ann_return / ann_vol if ann_vol else float("nan"),
        "mdd": max_drawdown(returns),
        "cum_return": nav - 1.0,
        "avg_turnover": float(daily["turnover"].mean()),
        "hit_rate": float((daily["net_return"] > 0).mean()),
    }


def backtest(prices: pd.DataFrame, symbols: list[str], cost_bps: float) -> pd.DataFrame:
    subset = prices[prices["ts_code"].isin(symbols)].copy()
    pivot = subset.pivot(index="date", columns="ts_code", values="close").sort_index()
    returns = pivot.pct_change(fill_method=None)
    cost_rate = cost_bps / 10000.0
    rows: list[dict[str, float | str | int]] = []
    previous: set[str] = set()
    for date, row in returns.iterrows():
        available = sorted([symbol for symbol in symbols if symbol in row.index and pd.notna(row[symbol])])
        if not available:
            continue
        current = set(available)
        if not previous:
            turnover = 1.0
        else:
            turnover = 0.5 * sum(abs((1 / len(current) if s in current else 0) - (1 / len(previous) if s in previous else 0)) for s in current | previous)
        gross = float(row[available].mean())
        net = gross - turnover * cost_rate
        rows.append(
            {
                "date": str(date),
                "n_available": len(available),
                "gross_return": gross,
                "turnover": turnover,
                "cost": turnover * cost_rate,
                "net_return": net,
            }
        )
        previous = current
    return pd.DataFrame(rows)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_local_fallback(symbols: list[str], start: str, end: str) -> pd.DataFrame:
    start_date = f"{start[:4]}-{start[4:6]}-{start[6:]}"
    end_date = f"{end[:4]}-{end[4:6]}-{end[6:]}"
    frames: list[pd.DataFrame] = []
    for path in [
        PROJECT_ROOT / "data/processed/cn_a_share/csi300_2025_2026/panel.csv",
        PROJECT_ROOT / "data/processed/cn_a_share/csi300_2018_2026_ytd/panel.csv",
    ]:
        if not path.exists():
            continue
        rows = []
        with path.open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                if row.get("ts_code") in symbols and start_date <= row["date"] <= end_date:
                    rows.append({"date": row["date"], "ts_code": row["ts_code"], "close": float(row["close"])})
        if rows:
            frames.append(pd.DataFrame(rows))
    if not frames:
        return pd.DataFrame(columns=["date", "ts_code", "close"])
    return pd.concat(frames, ignore_index=True).drop_duplicates(["date", "ts_code"], keep="first")


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    ak = load_akshare()
    frames = []
    failures = []
    for ts_code in DEFAULT_SYMBOLS:
        try:
            try:
                df = fetch_one(ak, ts_code, args.start, args.end, args.adjust)
            except Exception:
                df = fetch_one_tx(ak, ts_code, args.start, args.end, args.adjust)
            if df.empty:
                failures.append({"ts_code": ts_code, "reason": "empty"})
            else:
                frames.append(df)
                print(f"fetched {ts_code} rows={len(df)} latest={df['date'].max()}")
        except Exception as exc:  # external data source can fail per symbol
            failures.append({"ts_code": ts_code, "reason": str(exc)})
            print(f"failed {ts_code}: {exc}", file=sys.stderr)
        time.sleep(args.sleep)

    if not frames:
        prices = pd.DataFrame(columns=["date", "ts_code", "close"])
    else:
        prices = pd.concat(frames, ignore_index=True)
    missing_after_fetch = [symbol for symbol in DEFAULT_SYMBOLS if symbol not in set(prices["ts_code"])]
    local = load_local_fallback(missing_after_fetch, args.start, args.end)
    if not local.empty:
        print(f"local_fallback symbols={local['ts_code'].nunique()} rows={len(local)} latest={local['date'].max()}")
        prices = pd.concat([prices, local], ignore_index=True)
    if prices.empty:
        raise RuntimeError("no price data available from public source or local fallback")
    prices = prices.drop_duplicates(["date", "ts_code"], keep="first")
    prices.to_csv(out_dir / "prices.csv", index=False)
    if failures:
        write_csv(out_dir / "fetch_failures.csv", failures)

    summary_rows: list[dict[str, str]] = []
    for topn in [5, 10, 20, len(DEFAULT_SYMBOLS)]:
        basket = DEFAULT_SYMBOLS[:topn]
        daily = backtest(prices, basket, args.cost_bps)
        label = f"top{topn}" if topn != len(DEFAULT_SYMBOLS) else "all"
        daily_path = out_dir / f"{label}_daily.csv"
        daily.to_csv(daily_path, index=False)
        s = stats(daily)
        basket_prices = prices[prices["ts_code"].isin(basket)]
        latest_date = basket_prices["date"].max() if not basket_prices.empty else ""
        summary_rows.append(
            {
                "basket": label,
                "requested_count": str(topn),
                "covered_count": str(basket_prices["ts_code"].nunique()),
                "start": str(daily["date"].min()) if not daily.empty else "",
                "end": str(daily["date"].max()) if not daily.empty else "",
                "latest_price_date": str(latest_date),
                "cost_bps": f"{args.cost_bps:.2f}",
                "days": f"{s['days']:.0f}",
                "ann_return": f"{s['ann_return']:.8f}",
                "ann_vol": f"{s['ann_vol']:.8f}",
                "sharpe": f"{s['sharpe']:.8f}",
                "mdd": f"{s['mdd']:.8f}",
                "cum_return": f"{s['cum_return']:.8f}",
                "avg_turnover": f"{s['avg_turnover']:.8f}",
                "hit_rate": f"{s['hit_rate']:.8f}",
                "daily_source": str(daily_path.relative_to(PROJECT_ROOT)),
            }
        )

    write_csv(out_dir / "custom_a_share_basket_summary.csv", summary_rows)
    print(f"summary={out_dir / 'custom_a_share_basket_summary.csv'} rows={len(summary_rows)} failures={len(failures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

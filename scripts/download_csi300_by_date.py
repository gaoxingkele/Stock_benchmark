"""Download CSI300-oriented Tushare data by trading date.

This is more scalable than per-stock downloads for formal benchmark windows.
It downloads market-wide daily tables by date and filters to CSI300 later in
`build_cn_panel.py --universe-only`.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.tushare_client import TushareClient, append_table_csv, write_table_csv  # noqa: E402
from src.utils.env import load_project_env  # noqa: E402


FIELDS = {
    "trade_cal": "exchange,cal_date,is_open,pretrade_date",
    "stock_basic": "ts_code,symbol,name,area,industry,market,list_date",
    "index_weight": "index_code,con_code,trade_date,weight",
    "index_daily": "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount",
    "daily": "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount",
    "adj_factor": "ts_code,trade_date,adj_factor",
    "daily_basic": "ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm,pb,ps,ps_ttm,dv_ratio,dv_ttm,total_share,float_share,free_share,total_mv,circ_mv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", required=True, help="Start date in YYYYMMDD.")
    parser.add_argument("--end-date", required=True, help="End date in YYYYMMDD.")
    parser.add_argument("--index-code", default="000300.SH")
    parser.add_argument("--sleep", type=float, default=0.25)
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--out-dir",
        default=str(PROJECT_ROOT / "data" / "raw" / "tushare" / "csi300_by_date"),
    )
    return parser.parse_args()


def should_skip(path: Path, force: bool) -> bool:
    return path.exists() and path.stat().st_size > 0 and not force


def with_retry(fn: Callable[[], object], label: str, retries: int = 3, sleep: float = 2.0) -> object:
    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - retry boundary for remote API instability
            last_exc = exc
            if attempt >= retries:
                break
            wait = sleep * attempt
            print(f"{label}: retry {attempt}/{retries - 1} after error: {exc}; wait={wait:.1f}s")
            time.sleep(wait)
    assert last_exc is not None
    raise last_exc


def save_single(client: TushareClient, api_name: str, params: dict, out_path: Path, force: bool) -> int:
    if should_skip(out_path, force):
        return -1
    table = with_retry(lambda: client.query(api_name, params=params, fields=FIELDS[api_name]), api_name)
    write_table_csv(table, out_path)
    return len(table.items)


def load_open_dates(trade_cal_path: Path) -> list[str]:
    dates: list[str] = []
    with trade_cal_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("is_open") == "1":
                dates.append(row["cal_date"])
    return sorted(dates)


def append_by_dates(client: TushareClient, api_name: str, dates: list[str], path: Path, sleep: float, force: bool) -> int:
    if force and path.exists():
        path.unlink()
    if should_skip(path, force):
        return -1
    total = 0
    for i, trade_date in enumerate(dates, start=1):
        table = with_retry(
            lambda: client.query(api_name, params={"trade_date": trade_date}, fields=FIELDS[api_name]),
            f"{api_name}:{trade_date}",
        )
        append_table_csv(table, path)
        total += len(table.items)
        print(f"{api_name}: {i}/{len(dates)} {trade_date} rows={len(table.items)}")
        time.sleep(sleep)
    return total


def main() -> int:
    args = parse_args()
    load_project_env(PROJECT_ROOT)
    client = TushareClient()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    common_range = {"start_date": args.start_date, "end_date": args.end_date}
    outputs: list[tuple[str, int, Path]] = []

    base_jobs = [
        ("trade_cal", {"exchange": "SSE", **common_range}, out_dir / "trade_cal.csv"),
        ("stock_basic", {"exchange": "", "list_status": "L"}, out_dir / "stock_basic.csv"),
        ("index_weight", {"index_code": args.index_code, **common_range}, out_dir / "index_weight.csv"),
        ("index_daily", {"ts_code": args.index_code, **common_range}, out_dir / "index_daily.csv"),
    ]
    for api_name, params, path in base_jobs:
        rows = save_single(client, api_name, params, path, args.force)
        outputs.append((api_name, rows, path))
        time.sleep(args.sleep)

    dates = load_open_dates(out_dir / "trade_cal.csv")
    if not dates:
        raise RuntimeError("No open trading dates found")

    for api_name in ["daily", "adj_factor", "daily_basic"]:
        path = out_dir / f"{api_name}.csv"
        rows = append_by_dates(client, api_name, dates, path, args.sleep, args.force)
        outputs.append((api_name, rows, path))

    for api_name, rows, path in outputs:
        row_text = "skipped" if rows < 0 else f"rows={rows}"
        print(f"{api_name}: {row_text} path={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

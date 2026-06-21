"""Download a small Tushare China A-share sample.

This script is intentionally dependency-free so the data access path can be
validated before installing Qlib or other research dependencies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.tushare_client import TushareClient, write_table_csv, write_table_json  # noqa: E402
from src.utils.env import load_project_env  # noqa: E402


DEFAULT_TABLES = {
    "trade_cal": {
        "params": {"exchange": "SSE"},
        "fields": "exchange,cal_date,is_open,pretrade_date",
    },
    "stock_basic": {
        "params": {"exchange": "", "list_status": "L"},
        "fields": "ts_code,symbol,name,area,industry,market,list_date",
    },
    "index_daily": {
        "params": {"ts_code": "000300.SH"},
        "fields": "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount",
    },
    "daily": {
        "params": {"ts_code": "600519.SH"},
        "fields": "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount",
    },
    "adj_factor": {
        "params": {"ts_code": "600519.SH"},
        "fields": "ts_code,trade_date,adj_factor",
    },
    "daily_basic": {
        "params": {"ts_code": "600519.SH"},
        "fields": "ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,total_mv,circ_mv",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", default="20240102", help="Start date in YYYYMMDD.")
    parser.add_argument("--end-date", default="20240105", help="End date in YYYYMMDD.")
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "data" / "raw" / "tushare" / "sample"))
    parser.add_argument("--json", action="store_true", help="Also write JSON copies preserving Tushare fields/items.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_project_env(PROJECT_ROOT)
    client = TushareClient()
    out_dir = Path(args.out_dir)
    summary: list[tuple[str, int, Path]] = []

    for api_name, spec in DEFAULT_TABLES.items():
        params = dict(spec["params"])
        params["start_date"] = args.start_date
        params["end_date"] = args.end_date
        table = client.query(api_name, params=params, fields=spec["fields"])
        csv_path = out_dir / f"{api_name}.csv"
        write_table_csv(table, csv_path)
        if args.json:
            write_table_json(table, out_dir / f"{api_name}.json")
        summary.append((api_name, len(table.items), csv_path))

    for api_name, row_count, csv_path in summary:
        print(f"{api_name}: rows={row_count} path={csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


"""Download CSI300-oriented raw Tushare data.

The script is resume-friendly at file level: existing CSV files are skipped
unless `--force` is passed. For large date ranges, run in smaller windows to
respect Tushare rate limits and account permissions.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


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
    parser.add_argument("--index-code", default="000300.SH", help="Index code for universe and benchmark.")
    parser.add_argument("--max-stocks", type=int, default=0, help="Limit stock downloads for smoke tests. 0 means all.")
    parser.add_argument("--sleep", type=float, default=0.25, help="Seconds to sleep between API calls.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output files.")
    parser.add_argument(
        "--out-dir",
        default=str(PROJECT_ROOT / "data" / "raw" / "tushare" / "csi300"),
        help="Output directory for raw CSV files.",
    )
    return parser.parse_args()


def should_skip(path: Path, force: bool) -> bool:
    return path.exists() and path.stat().st_size > 0 and not force


def save_single(client: TushareClient, api_name: str, params: dict, out_path: Path, force: bool) -> int:
    if should_skip(out_path, force):
        return -1
    table = client.query(api_name, params=params, fields=FIELDS[api_name])
    write_table_csv(table, out_path)
    return len(table.items)


def load_codes(index_weight_csv: Path, max_stocks: int) -> list[str]:
    import csv

    codes: list[str] = []
    seen: set[str] = set()
    with index_weight_csv.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row.get("con_code", "").strip()
            if code and code not in seen:
                seen.add(code)
                codes.append(code)
                if max_stocks and len(codes) >= max_stocks:
                    break
    return codes


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

    codes = load_codes(out_dir / "index_weight.csv", args.max_stocks)
    if not codes:
        raise RuntimeError("No CSI300 constituent codes found in index_weight.csv")

    stock_jobs = [
        ("daily", out_dir / "daily.csv"),
        ("adj_factor", out_dir / "adj_factor.csv"),
        ("daily_basic", out_dir / "daily_basic.csv"),
    ]
    for api_name, path in stock_jobs:
        if args.force and path.exists():
            path.unlink()
        total = 0
        if should_skip(path, args.force):
            outputs.append((api_name, -1, path))
            continue
        for i, code in enumerate(codes, start=1):
            table = client.query(api_name, params={"ts_code": code, **common_range}, fields=FIELDS[api_name])
            append_table_csv(table, path)
            total += len(table.items)
            print(f"{api_name}: {i}/{len(codes)} {code} rows={len(table.items)}")
            time.sleep(args.sleep)
        outputs.append((api_name, total, path))

    for api_name, rows, path in outputs:
        row_text = "skipped" if rows < 0 else f"rows={rows}"
        print(f"{api_name}: {row_text} path={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


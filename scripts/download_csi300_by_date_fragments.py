"""Download CSI300 Tushare data with per-date fragment caching.

This script writes the same final raw files expected by `build_cn_panel.py`,
but date-based tables are cached under `_fragments/<api_name>/<trade_date>.csv`
before being merged. This makes long formal windows resumable after network or
rate-limit failures.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.tushare_client import TushareClient, TushareTable, write_table_csv  # noqa: E402
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
DATE_TABLES = ["daily", "adj_factor", "daily_basic"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", required=True, help="Start date in YYYYMMDD.")
    parser.add_argument("--end-date", required=True, help="End date in YYYYMMDD.")
    parser.add_argument("--index-code", default="000300.SH")
    parser.add_argument("--sleep", type=float, default=0.35)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-sleep", type=float, default=2.0)
    parser.add_argument("--force-base", action="store_true", help="Redownload non-date base files.")
    parser.add_argument("--force-fragments", action="store_true", help="Redownload per-date fragments.")
    parser.add_argument("--max-fragment-dates", type=int, help="Download at most N missing date fragments per date table.")
    parser.add_argument("--complete-triplet-batch", type=int, help="Advance the first N incomplete dates across all date tables.")
    parser.add_argument("--continue-on-error", action="store_true", help="Record failed fragments and keep downloading other dates.")
    parser.add_argument("--merge-only", action="store_true", help="Merge existing fragments without calling Tushare.")
    parser.add_argument(
        "--out-dir",
        default=str(PROJECT_ROOT / "data" / "raw" / "tushare" / "csi300_by_date"),
    )
    return parser.parse_args()


def with_retry(fn: Callable[[], TushareTable], label: str, retries: int = 3, sleep: float = 2.0) -> TushareTable:
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


def should_skip(path: Path, force: bool) -> bool:
    return path.exists() and path.stat().st_size > 0 and not force


def save_base(client: TushareClient, api_name: str, params: dict, path: Path, force: bool) -> int:
    if should_skip(path, force):
        return -1
    table = with_retry(lambda: client.query(api_name, params=params, fields=FIELDS[api_name]), api_name)
    write_table_csv(table, path)
    return len(table.items)


def load_open_dates(trade_cal_path: Path) -> list[str]:
    with trade_cal_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return sorted(row["cal_date"] for row in reader if row.get("is_open") == "1")


def read_csv_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    if not rows:
        return [], []
    return rows[0], rows[1:]


def merge_fragments(api_name: str, dates: list[str], out_dir: Path) -> tuple[int, int]:
    fragment_dir = out_dir / "_fragments" / api_name
    out_path = out_dir / f"{api_name}.csv"
    missing = 0
    total_rows = 0
    header: list[str] | None = None
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        for trade_date in dates:
            fragment_path = fragment_dir / f"{trade_date}.csv"
            if not fragment_path.exists() or fragment_path.stat().st_size == 0:
                missing += 1
                continue
            fragment_header, rows = read_csv_rows(fragment_path)
            if header is None:
                header = fragment_header
                writer.writerow(header)
            elif fragment_header != header:
                raise RuntimeError(f"header mismatch in {fragment_path}")
            writer.writerows(rows)
            total_rows += len(rows)
    return total_rows, missing


def save_manifest(out_dir: Path, payload: dict) -> None:
    manifest_path = out_dir / "fragment_download_manifest.json"
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def download_fragments(
    client: TushareClient,
    api_name: str,
    dates: list[str],
    out_dir: Path,
    sleep: float,
    force: bool,
    max_fragment_dates: int | None,
    retries: int,
    retry_sleep: float,
    continue_on_error: bool,
) -> tuple[int, int, list[dict[str, str]]]:
    fragment_dir = out_dir / "_fragments" / api_name
    fragment_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    skipped = 0
    errors: list[dict[str, str]] = []
    for i, trade_date in enumerate(dates, start=1):
        fragment_path = fragment_dir / f"{trade_date}.csv"
        if should_skip(fragment_path, force):
            skipped += 1
            continue
        if max_fragment_dates is not None and downloaded >= max_fragment_dates:
            continue
        try:
            table = with_retry(
                lambda: client.query(api_name, params={"trade_date": trade_date}, fields=FIELDS[api_name]),
                f"{api_name}:{trade_date}",
                retries=retries,
                sleep=retry_sleep,
            )
        except Exception as exc:  # noqa: BLE001 - long downloads should be able to continue by date
            if not continue_on_error:
                raise
            errors.append({"api_name": api_name, "trade_date": trade_date, "error": str(exc)})
            print(f"{api_name}: {i}/{len(dates)} {trade_date} error={exc}")
            time.sleep(sleep)
            continue
        write_table_csv(table, fragment_path)
        downloaded += 1
        print(f"{api_name}: {i}/{len(dates)} {trade_date} rows={len(table.items)}")
        time.sleep(sleep)
    return downloaded, skipped, errors


def existing_fragment_dates(out_dir: Path, api_name: str) -> set[str]:
    fragment_dir = out_dir / "_fragments" / api_name
    if not fragment_dir.exists():
        return set()
    return {path.stem for path in fragment_dir.glob("*.csv") if path.stat().st_size > 0}


def triplet_batch_dates(out_dir: Path, dates: list[str], batch_size: int | None) -> list[str]:
    if batch_size is None:
        return dates
    completed_by_table = {api_name: existing_fragment_dates(out_dir, api_name) for api_name in DATE_TABLES}
    selected: list[str] = []
    for trade_date in dates:
        if all(trade_date in completed_by_table[api_name] for api_name in DATE_TABLES):
            continue
        selected.append(trade_date)
        if len(selected) >= batch_size:
            break
    return selected


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    common_range = {"start_date": args.start_date, "end_date": args.end_date}
    client: TushareClient | None = None

    if not args.merge_only:
        load_project_env(PROJECT_ROOT)
        client = TushareClient()
        base_jobs = [
            ("trade_cal", {"exchange": "SSE", **common_range}, out_dir / "trade_cal.csv"),
            ("stock_basic", {"exchange": "", "list_status": "L"}, out_dir / "stock_basic.csv"),
            ("index_weight", {"index_code": args.index_code, **common_range}, out_dir / "index_weight.csv"),
            ("index_daily", {"ts_code": args.index_code, **common_range}, out_dir / "index_daily.csv"),
        ]
        for api_name, params, path in base_jobs:
            rows = save_base(client, api_name, params, path, args.force_base)
            row_text = "skipped" if rows < 0 else f"rows={rows}"
            print(f"{api_name}: {row_text} path={path}")
            time.sleep(args.sleep)

    dates = load_open_dates(out_dir / "trade_cal.csv")
    if not dates:
        raise RuntimeError("No open trading dates found")
    download_dates = triplet_batch_dates(out_dir, dates, args.complete_triplet_batch)

    manifest: dict[str, object] = {
        "start_date": args.start_date,
        "end_date": args.end_date,
        "index_code": args.index_code,
        "open_dates": len(dates),
        "selected_download_dates": download_dates,
        "date_tables": {},
    }
    for api_name in DATE_TABLES:
        if args.merge_only:
            downloaded, skipped, errors = 0, 0, []
        else:
            assert client is not None
            downloaded, skipped, errors = download_fragments(
                client,
                api_name,
                download_dates,
                out_dir,
                args.sleep,
                args.force_fragments,
                args.max_fragment_dates,
                args.retries,
                args.retry_sleep,
                args.continue_on_error,
            )
        total_rows, missing = merge_fragments(api_name, dates, out_dir)
        manifest["date_tables"][api_name] = {
            "downloaded_fragments": downloaded,
            "skipped_fragments": skipped,
            "merged_rows": total_rows,
            "missing_fragments": missing,
            "errors": errors,
            "merged_path": str(out_dir / f"{api_name}.csv"),
        }
        print(f"{api_name}: merged_rows={total_rows} missing_fragments={missing} errors={len(errors)}")

    save_manifest(out_dir, manifest)
    print(f"manifest={out_dir / 'fragment_download_manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

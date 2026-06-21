# Data Pipeline

Date: 2026-06-19

## Current Status

The first Tushare access path and a CSI300 smoke pipeline are implemented and verified.

Script:

```bash
python Stock_benchmark/scripts/download_tushare_sample.py --start-date 20240102 --end-date 20240105 --json
```

Verified output:

```text
data/raw/tushare/sample/trade_cal.csv
data/raw/tushare/sample/stock_basic.csv
data/raw/tushare/sample/index_daily.csv
data/raw/tushare/sample/daily.csv
data/raw/tushare/sample/adj_factor.csv
data/raw/tushare/sample/daily_basic.csv
```

CSI300 smoke command:

```bash
python Stock_benchmark/scripts/download_csi300_tushare.py \
  --start-date 20240102 \
  --end-date 20240105 \
  --max-stocks 5 \
  --sleep 0.1 \
  --force \
  --out-dir Stock_benchmark/data/raw/tushare/csi300_smoke

python Stock_benchmark/scripts/build_cn_panel.py \
  --raw-dir Stock_benchmark/data/raw/tushare/csi300_smoke \
  --out-dir Stock_benchmark/data/processed/cn_a_share/csi300_smoke
```

Verified CSI300 smoke output:

```text
data/raw/tushare/csi300_smoke/index_weight.csv    300 rows
data/raw/tushare/csi300_smoke/daily.csv            20 rows
data/raw/tushare/csi300_smoke/adj_factor.csv       20 rows
data/raw/tushare/csi300_smoke/daily_basic.csv      20 rows
data/processed/cn_a_share/csi300_smoke/panel.csv   20 rows, 5 symbols
data/processed/cn_a_share/csi300_smoke/qlib_csv/   5 per-symbol CSV files
```

CSI300 by-date smoke command:

```bash
python Stock_benchmark/scripts/download_csi300_by_date.py \
  --start-date 20240102 \
  --end-date 20240110 \
  --sleep 0.1 \
  --force \
  --out-dir Stock_benchmark/data/raw/tushare/csi300_by_date_smoke

python Stock_benchmark/scripts/build_cn_panel.py \
  --raw-dir Stock_benchmark/data/raw/tushare/csi300_by_date_smoke \
  --out-dir Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke \
  --universe-only
```

Verified by-date smoke output:

```text
raw daily.csv             37,319 rows
raw adj_factor.csv        37,555 rows
raw daily_basic.csv       37,319 rows
processed panel.csv        2,100 rows, 300 symbols
processed qlib_csv/          300 per-symbol CSV files
processed qlib_bin_numeric/  300 feature directories
```

The sample uses:

- Calendar: SSE
- Index: `000300.SH`
- Single stock sanity check: `600519.SH`
- Window: 2024-01-02 to 2024-01-05

## Implemented Code

| File | Purpose |
| --- | --- |
| `src/utils/env.py` | Loads `.env` and `.env.cloubic` without printing secrets. |
| `src/data/tushare_client.py` | Minimal dependency-free Tushare HTTP client and CSV/JSON writers. |
| `scripts/download_tushare_sample.py` | Downloads a small China A-share sample to validate API and storage layout. |
| `scripts/download_csi300_tushare.py` | Downloads CSI300-oriented raw data with resumable file-level behavior. |
| `scripts/download_csi300_by_date_fragments.py` | Downloads market-wide date tables into per-date fragments for long-window resumability. |
| `scripts/build_cn_panel.py` | Builds adjusted panel data, Qlib-friendly CSV files, calendars, and instruments. |
| `scripts/validate_tushare_raw_dataset.py` | Checks raw Tushare files before panel construction. |
| `scripts/report_tushare_fragment_progress.py` | Reports staged fragment progress for long Tushare downloads. |

Long-window downloads should use `--complete-triplet-batch` to keep `daily`, `adj_factor`, and `daily_basic` aligned by trade date.
| `configs/cn_a_share_csi300_sample.json` | First CSI300 benchmark configuration stub. |

## Qlib CSV To Bin

Qlib's converter is available at:

```text
external_repos/microsoft__qlib/scripts/dump_bin.py
```

Expected next command shape after dependencies are installed:

```bash
python Stock_benchmark/external_repos/microsoft__qlib/scripts/dump_bin.py dump_all \
  --data_path Stock_benchmark/data/processed/cn_a_share/csi300_smoke/qlib_csv \
  --qlib_dir Stock_benchmark/data/processed/cn_a_share/csi300_smoke/qlib_bin \
  --freq day \
  --date_field_name date \
  --symbol_field_name symbol
```

Status: conversion has been verified on `csi300_smoke` and the formal `csi300_2018_2024` profile.

```text
data/processed/cn_a_share/csi300_smoke/qlib_bin_numeric/
```

Use `--include_fields` to avoid exporting string columns such as `symbol` and `ts_code`.

## Next Data Tasks

1. Install or create the Qlib runtime environment.
2. Convert `qlib_csv/` to Qlib bin format with `dump_bin.py`.
3. Run the formal CSI300 2018-2024 dataset profile in `docs/benchmark_design/formal_csi300_dataset.md`.
4. Add resume-safe raw cache naming by API, date range, and parameter hash.
5. Add suspension and limit-up/down tradability filters where Tushare permissions allow it.
6. Run LightGBM on the generated Qlib data.

## Smoke Experiments

Factor IC smoke:

```bash
python Stock_benchmark/scripts/evaluate_factor_smoke.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_smoke/panel.csv \
  --score-field pct_chg \
  --horizon 1 \
  --out Stock_benchmark/experiments/baselines/factor_smoke_csi300.csv
```

Verified result:

```text
rows=15, dates=3
summary IC=0.48471902, RankIC=0.46666667
```

LightGBM smoke:

```bash
python Stock_benchmark/scripts/run_lightgbm_smoke.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_smoke/panel.csv \
  --train-end 2024-01-03 \
  --out Stock_benchmark/experiments/baselines/lightgbm_smoke_csi300.csv
```

Verified result:

```text
train_rows=10, test_rows=5
summary IC=0.17806285, RankIC=-0.15389675
```

Larger by-date CSI300 smoke:

```bash
python Stock_benchmark/scripts/evaluate_factor_smoke.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --score-field pct_chg \
  --horizon 1 \
  --out Stock_benchmark/experiments/baselines/factor_smoke_csi300_by_date.csv

python Stock_benchmark/scripts/run_lightgbm_smoke.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --train-end 2024-01-05 \
  --out Stock_benchmark/experiments/baselines/lightgbm_smoke_csi300_by_date.csv
```

Verified result:

```text
factor smoke: rows=1800, dates=6, IC=0.26386290, RankIC=0.28637491
LightGBM smoke: train_rows=1144, test_rows=572, IC=0.02623058, RankIC=0.05295324
```

Fragment downloader smoke:

```bash
python Stock_benchmark/scripts/download_csi300_by_date_fragments.py \
  --start-date 20240102 \
  --end-date 20240103 \
  --sleep 0.1 \
  --out-dir Stock_benchmark/data/raw/tushare/csi300_fragment_smoke

python Stock_benchmark/scripts/validate_tushare_raw_dataset.py \
  --raw-dir Stock_benchmark/data/raw/tushare/csi300_fragment_smoke

python Stock_benchmark/scripts/build_cn_panel.py \
  --raw-dir Stock_benchmark/data/raw/tushare/csi300_fragment_smoke \
  --out-dir Stock_benchmark/data/processed/cn_a_share/csi300_fragment_smoke \
  --universe-only
```

Verified result:

```text
open_dates=2
daily.csv rows=10659
adj_factor.csv rows=10729
daily_basic.csv rows=10659
processed panel rows=600, symbols=300
```

## Notes

- The sample script intentionally uses only Python standard library modules.
- Full historical downloads should be rate-limited and resumable.
- The raw Tushare response can be stored as JSON when exact field order needs to be preserved.

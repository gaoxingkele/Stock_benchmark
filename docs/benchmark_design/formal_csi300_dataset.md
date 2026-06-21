# Formal CSI300 Dataset Profile

The first formal China A-share benchmark profile is CSI300 daily data from 2018-01-02 to 2024-12-31.

## Configs

```text
configs/datasets/csi300_2018_2024_tushare.json
configs/universes/csi300_2018_2024.json
configs/splits/csi300_2018_2024.json
```

## Split

```text
train: 2018-01-02 to 2021-12-31
valid: 2022-01-04 to 2022-12-30
test:  2023-01-03 to 2024-12-31
```

Label horizons:

```text
1 trading day
5 trading days
```

## Download

```bash
python Stock_benchmark/scripts/download_csi300_by_date_fragments.py \
  --start-date 20180102 \
  --end-date 20241231 \
  --sleep 0.35 \
  --out-dir Stock_benchmark/data/raw/tushare/csi300_2018_2024
```

The downloader caches date-based tables under `_fragments/<api_name>/<trade_date>.csv` and then merges them into `daily.csv`, `adj_factor.csv`, and `daily_basic.csv`.

If a long run stops, rerun the same command. Existing non-empty fragments are skipped. To rebuild merged CSVs without calling Tushare:

```bash
python Stock_benchmark/scripts/download_csi300_by_date_fragments.py \
  --start-date 20180102 \
  --end-date 20241231 \
  --merge-only \
  --out-dir Stock_benchmark/data/raw/tushare/csi300_2018_2024
```

Validate raw files before panel construction:

```bash
python Stock_benchmark/scripts/validate_tushare_raw_dataset.py \
  --raw-dir Stock_benchmark/data/raw/tushare/csi300_2018_2024
```

For staged downloads, report fragment progress:

```bash
python Stock_benchmark/scripts/report_tushare_fragment_progress.py \
  --raw-dir Stock_benchmark/data/raw/tushare/csi300_2018_2024
```

Recommended incremental batch command:

```bash
python Stock_benchmark/scripts/download_csi300_by_date_fragments.py \
  --start-date 20180102 \
  --end-date 20241231 \
  --sleep 0.5 \
  --retries 5 \
  --retry-sleep 3 \
  --complete-triplet-batch 25 \
  --continue-on-error \
  --out-dir Stock_benchmark/data/raw/tushare/csi300_2018_2024
```

On Windows PowerShell, the helper script is:

```powershell
powershell -ExecutionPolicy Bypass -File Stock_benchmark/scripts/continue_formal_csi300_download.ps1 -BatchSize 50
```

## Build Panel

```bash
python Stock_benchmark/scripts/build_cn_panel.py \
  --raw-dir Stock_benchmark/data/raw/tushare/csi300_2018_2024 \
  --out-dir Stock_benchmark/data/processed/cn_a_share/csi300_2018_2024 \
  --adjust forward \
  --universe-only
```

## Qlib Conversion

Use the same numeric field list as the smoke conversion:

```text
open,high,low,close,pre_close,volume,amount,change,pct_chg,turnover_rate,volume_ratio,pe,pb,total_mv,circ_mv,factor
```

The formal Qlib LightGBM and paper-model configs should target:

```text
data/processed/cn_a_share/csi300_2018_2024/qlib_bin_numeric/
```

## Status

This profile is downloaded, validated, processed, and converted to Qlib numeric bin format. The fragment downloader was first verified on a two-trading-day Tushare smoke run:

```text
raw_dir=data/raw/tushare/csi300_fragment_smoke
open_dates=2
daily.csv rows=10659
adj_factor.csv rows=10729
daily_basic.csv rows=10659
processed panel rows=600, symbols=300
```

Current staged formal raw progress:

```text
open_dates=1699
daily fragments=1699
adj_factor fragments=1699
daily_basic fragments=1699
complete date triplets=1699
next incomplete date=
daily.csv rows=7499987
adj_factor.csv rows=7745206
daily_basic.csv rows=7435252
processed panel rows=514449, symbols=328
labels_h1 rows=514121
labels_h5 rows=512809
```

The formal Qlib LightGBM workflow file prerequisites validate against:

```text
data/processed/cn_a_share/csi300_2018_2024/qlib_bin_numeric/
```

Full Qlib runtime execution still requires resolving the local compiled Qlib dependency issue.

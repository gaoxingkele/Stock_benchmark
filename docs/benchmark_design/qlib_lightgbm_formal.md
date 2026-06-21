# Formal Qlib LightGBM Workflow

Formal config:

```text
configs/qlib/workflow_lightgbm_csi300_2018_2024.yaml
```

It targets the formal CSI300 2018-2024 dataset profile:

```text
data/processed/cn_a_share/csi300_2018_2024/qlib_bin_numeric/
```

Split:

```text
train: 2018-01-02 to 2021-12-31
valid: 2022-01-04 to 2022-12-30
test:  2023-01-03 to 2024-12-31
```

Validate YAML structure before the formal data exists:

```bash
python Stock_benchmark/scripts/validate_qlib_workflow_config.py \
  Stock_benchmark/configs/qlib/workflow_lightgbm_csi300_2018_2024.yaml \
  --allow-missing-data
```

Run prerequisite order:

1. Download raw data with `download_csi300_by_date_fragments.py`.
2. Validate raw files with `validate_tushare_raw_dataset.py`.
3. Build panel and Qlib CSV files with `build_cn_panel.py`.
4. Convert Qlib CSV to bin with Qlib `dump_bin.py`.
5. Install or activate a working Qlib runtime.
6. Run this workflow as the formal LightGBM baseline, or use the direct runner below when the mlflow workflow layer is unavailable.

## Direct Qlib DataHandler Run

The full `qlib.cli.run` workflow currently requires missing optional workflow dependencies (`jinja2`, `mlflow`). To validate the Qlib data provider and baseline model without the mlflow recorder layer, use:

```bash
python Stock_benchmark/scripts/run_qlib_lightgbm_direct.py \
  Stock_benchmark/configs/qlib/workflow_lightgbm_csi300_2018_2024.yaml \
  --out Stock_benchmark/experiments/baselines/qlib_direct_lightgbm_csi300_2018_2024_h1.csv \
  --num-boost-round 120 \
  --early-stopping-rounds 20
```

This runner uses Qlib `DataHandlerLP` and `DatasetH` against:

```text
data/processed/cn_a_share/csi300_2018_2024/qlib_bin_numeric/
```

It bypasses only Qlib's mlflow workflow recorder.

Verified result:

```text
train_rows=278372
valid_rows=77544
test_rows=158478
SUMMARY IC=-0.00582856 RankIC=0.00022628 ICIR=-0.05284884 RankICIR=0.00221945
```

## Runtime Notes

Two local runtime shims are currently used:

```text
external_repos/microsoft__qlib/qlib/data/_libs/rolling.py
external_repos/microsoft__qlib/qlib/data/_libs/expanding.py
```

They provide pure Python fallbacks for the missing compiled Cython rolling operators. These are slower than Qlib's native extensions but sufficient for the current formal baseline.

Current status: formal Qlib provider/data baseline is runnable through the direct runner. Full `qlib.cli.run` workflow remains pending until `jinja2` and `mlflow` are installed or otherwise provided.

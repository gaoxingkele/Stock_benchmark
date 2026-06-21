# Qlib LightGBM Smoke Workflow

Local config:

```text
configs/qlib/workflow_lightgbm_csi300_by_date_smoke.yaml
```

It targets:

```text
data/processed/cn_a_share/csi300_by_date_smoke/qlib_bin_numeric/
```

The config uses `DataHandlerLP` plus a `QlibDataLoader` over the converted local fields:

```text
open, high, low, close, pre_close, volume, amount, change, pct_chg,
turnover_rate, volume_ratio, pe, pb, total_mv, circ_mv, factor
```

Label:

```text
Ref($close, -2) / Ref($close, -1) - 1
```

This matches the one-day forward return convention used by the local smoke scripts.

## Validation

Validate file-level prerequisites without importing Qlib:

```bash
python Stock_benchmark/scripts/validate_qlib_workflow_config.py \
  Stock_benchmark/configs/qlib/workflow_lightgbm_csi300_by_date_smoke.yaml
```

## Runtime Status

The workflow config is prepared, but a formal Qlib run is still blocked in the current Python environment because `pyqlib` cannot import its compiled rolling extension:

```text
ModuleNotFoundError: No module named 'qlib.data._libs.rolling'
```

The local editable install also requires Microsoft C++ Build Tools. Until that runtime is available, this project uses the standalone LightGBM smoke script for executable baseline verification and keeps this Qlib config ready for the formal environment.

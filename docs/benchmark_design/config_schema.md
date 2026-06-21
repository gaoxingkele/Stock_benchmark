# Benchmark Config Schema

Benchmark experiments use JSON files under `configs/experiments/`.

The schema is intentionally small so paper-specific projects can share the same dataset, split, label, and metric definitions without taking a dependency on Qlib internals.

## Required Top-Level Fields

| Field | Purpose |
| --- | --- |
| `id` | Stable experiment identifier. |
| `task` | `trend_prediction` or `alpha_factor`. |
| `market` | Current benchmark supports `cn_a_share`. |
| `universe` | Universe name, index code, and selection rule. |
| `data` | Provider, frequency, panel path, and roots. |
| `features` | Feature source and feature columns. |
| `label` | Label type and forecast horizon. |
| `split` | Train, optional validation, and test windows. |
| `model` | Model family, name, and parameters. |
| `evaluation` | Metrics and grouping rule. |
| `outputs` | Result CSV and summary report locations. |

## Validation

```bash
python Stock_benchmark/scripts/validate_benchmark_config.py \
  Stock_benchmark/configs/experiments/csi300_by_date_smoke_lightgbm.json
```

The first checked config is:

```text
configs/experiments/csi300_by_date_smoke_lightgbm.json
```

It points to the 300-symbol CSI300 by-date smoke panel and the existing LightGBM smoke output.

## Running A Configured Smoke Experiment

```bash
python Stock_benchmark/scripts/run_lightgbm_smoke.py \
  --config Stock_benchmark/configs/experiments/csi300_by_date_smoke_lightgbm.json
```

Current verified summary:

```text
test_rows=572
IC=0.02623058
RankIC=0.05295324
ICIR=0.26715893
RankICIR=1.88916703
```

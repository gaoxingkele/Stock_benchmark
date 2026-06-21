# Local Project Evidence

## README.md

```text
# 2021 TCTS Wu

## Paper

- Title: Temporally Correlated Task Scheduling for Sequence Learning
- Authors: Xueqing Wu et al.
- Year: 2021
- Venue: ICML 2021 according to Qlib model zoo
- Code: `external_repos/microsoft__qlib/examples/benchmarks/TCTS`

## Benchmark Role

Transformer-style CCF-A time-series baseline available in Qlib's alpha benchmark pool.

## Status

- PDF URL still needs source verification.
- Code repository cloned through `microsoft/qlib`.

```

## notes.md

```text
# TCTS Notes

## Source Verification

- Paper: Temporally Correlated Task Scheduling for Sequence Learning.
- Venue: ICML 2021, PMLR 139.
- PDF: `https://proceedings.mlr.press/v139/wu21e/wu21e.pdf`.
- Reproduction code referenced by Qlib: `https://github.com/lwwang1995/tcts`.
- Qlib baseline code: `external_repos/microsoft__qlib/examples/benchmarks/TCTS`.

## Core Idea

TCTS treats sequence forecasting as a multi-task problem where auxiliary tasks are temporally correlated with the main task. In stock forecasting, these tasks correspond to returns at different future horizons. A learnable scheduler selects which auxiliary task should guide training at each step, and the forecasting model plus scheduler are optimized through a bilevel training process.

## Qlib Setting

The local Qlib benchmark config uses:

```text
external_repos/microsoft__qlib/examples/benchmarks/TCTS/workflow_config_tcts_Alpha360.yaml
```

The Qlib config defines three labels:

```text
Ref($close, -2) / Ref($close, -1) - 1
Ref($close, -3) / Ref($close, -1) - 1
Ref($close, -4) / Ref($close, -1) - 1
```

For the China A-share benchmark, the first smoke config is recorded at:

```text
configs/china_a_share_smoke.json
```

## Reproduction Notes

- Start from the same CSI300 provider as LightGBM and TRA.
- Use TCTS after a vanilla Transformer baseline, because TCTS adds a scheduler on top of multi-horizon sequence learning.
- The current 7-trading-day smoke sample can validate config wiring but is too short for a meaningful multi-horizon TCTS run.

```

## repo_analysis.md

```text
# TCTS Repository Analysis

## Repository

`microsoft/qlib`

## Status

Cloned locally at:

```text
external_repos/microsoft__qlib
```

## Notes

- Qlib benchmark README reports TCTS Alpha360 results.
- The base model is noted as GRU in the Qlib benchmark README.


```

## reproduction_plan.md

```text
# TCTS Reproduction Plan

## Local Code Entrypoints

```text
external_repos/microsoft__qlib/examples/benchmarks/TCTS/
```

First config:

```text
examples/benchmarks/TCTS/workflow_config_tcts_Alpha360.yaml
```

## China A-Share Adaptation

1. Use as a strong Transformer-style baseline after LightGBM and Transformer.
2. Run on the same CSI300 Alpha360 feature set as TRA.
3. Keep paper URL/venue metadata verification as a source-collection task.

## Expected Outputs

- Shared alpha metrics.
- Comparison against vanilla Transformer, TRA, and MASTER.


```

## configs/china_a_share_smoke.json

```text
{
  "paper_id": "2021_tcts_wu",
  "model": "TCTS",
  "task": "trend_prediction",
  "market": "cn_a_share",
  "universe_config": "Stock_benchmark/configs/universes/csi300_smoke.json",
  "split_config": "Stock_benchmark/configs/splits/csi300_by_date_smoke.json",
  "data": {
    "panel": "Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv",
    "qlib_provider_uri": "Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/qlib_bin_numeric",
    "labels": {
      "h1": "Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/labels_h1.csv",
      "h5": "Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/labels_h5.csv"
    }
  },
  "upstream": {
    "repo": "Stock_benchmark/external_repos/microsoft__qlib",
    "workflow": "examples/benchmarks/TCTS/workflow_config_tcts_Alpha360.yaml"
  },
  "first_target": {
    "feature_handler": "Alpha360",
    "label": "h1 smoke, then multi-horizon formal",
    "baseline_before_run": "Transformer and TRA on the same provider_uri"
  },
  "blocked_by": [
    "Full pyqlib runtime is unavailable in the current Python environment.",
    "Paper URL and venue metadata still need verification before final literature notes."
  ]
}

```

## configs/china_a_share_formal.json

```text
{
  "paper_id": "2021_tcts_wu",
  "model": "TCTS",
  "task": "trend_prediction",
  "market": "cn_a_share",
  "universe_config": "Stock_benchmark/configs/universes/csi300_2018_2024.json",
  "split_config": "Stock_benchmark/configs/splits/csi300_2018_2024.json",
  "data": {
    "panel": "Stock_benchmark/data/processed/cn_a_share/csi300_2018_2024/panel.csv",
    "qlib_provider_uri": "Stock_benchmark/data/processed/cn_a_share/csi300_2018_2024/qlib_bin_numeric",
    "labels": {
      "h1": "Stock_benchmark/data/processed/cn_a_share/csi300_2018_2024/labels_h1.csv",
      "h5": "Stock_benchmark/data/processed/cn_a_share/csi300_2018_2024/labels_h5.csv"
    }
  },
  "first_runnable": {
    "script": "Stock_benchmark/scripts/run_paper_model_baseline.py",
    "mode": "tcts",
    "lookback": 20,
    "max_train_rows": 50000,
    "outputs": {
      "h1": "Stock_benchmark/experiments/paper_runs/tcts_formal_csi300_2018_2024_h1.csv",
      "h5": "Stock_benchmark/experiments/paper_runs/tcts_formal_csi300_2018_2024_h5.csv"
    }
  },
  "official_runtime_status": "Blocked until PyTorch/Qlib runtime is provisioned."
}

```

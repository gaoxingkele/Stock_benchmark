# Local Project Evidence

## README.md

```text
# 2023 DoubleAdapt Zhao

## Paper

- Title: DoubleAdapt: A Meta-learning Approach to Incremental Learning for Stock Trend Forecasting
- Authors: Lifan Zhao; Shuming Kong; Yanyan Shen
- Year: 2023
- Venue: KDD 2023
- PDF: https://arxiv.org/abs/2306.09862
- Local PDF: `papers/raw/2023_doubleadapt_zhao.pdf`
- Code: `external_repos/SJTU-DMTai__qlib/examples/benchmarks_dynamic/incremental`

## Benchmark Role

Core CCF-A dynamic adaptation model for stock trend forecasting and concept drift.

## Status

- PDF downloaded and header verified.
- Code repository cloned through `SJTU-DMTai/qlib`.

```

## notes.md

```text
# DoubleAdapt Notes

## Core Problem

DoubleAdapt targets incremental learning for stock trend forecasting under concept drift. It starts from the observation that stock data arrives continuously, and online systems need efficient updates without full rolling retraining.

## Method

The framework uses two adapters:

- Data adapter: transforms incremental data and test data toward a locally stationary distribution.
- Model adapter: learns task-specific parameter initialization for the forecast model.

The paper casts each incremental learning task as a meta-learning task. The adapters are optimized so that updates on recent incremental data generalize better to future test data.

## Motivation

Rolling retraining can be accurate but expensive and often wastes recent validation data. Naive incremental learning is efficient but fragile under distribution shifts between recent incremental data and future test data.

DoubleAdapt mitigates this by adapting both:

- the data distribution used for the update;
- the model initialization before the update.

## Data

Paper/code setting:

- Chinese stock market.
- CSI300 is explicitly used in examples and distribution-shift visualization.
- Qlib crowd-source data is recommended by the repo.
- Supports `--data_dir crowd_data` and `--data_dir cn_data`.
- Supports `--alpha 360` or `--alpha 158`.

Project adaptation:

- Start from CSI300 Tushare data.
- Need longer windows than smoke data to define incremental tasks.
- First practical split should include monthly retraining windows and 2-3 trading day adaptation tests.

## Labels

Repo README emphasizes:

- The task is stock trend prediction, not necessarily rank prediction.
- Uses `CSZScoreNorm` instead of `CSRankNorm` for non-rank labels.
- `--rank_label False` is recommended for default DoubleAdapt.
- If `--rank_label True`, the README recommends `--adapt_y False`.

Important label expression:

```text
Ref($close, -horizon-1) / Ref($close, -1) - 1
```

The implementation requires `step > horizon`; recommended example is `--step 5 --horizon 1`.

## Metrics

Use shared forecast and portfolio metrics:

- IC
- RankIC
- ICIR
- RankICIR
- MSE/MAE if available from workflow
- Portfolio return metrics for comparable strategy backtests

For incremental learning, also record:

- update interval
- training time per update
- memory use
- comparison against rolling retraining and naive incremental learning

## Code Entrypoints

```text
external_repos/SJTU-DMTai__qlib/examples/benchmarks_dynamic/incremental/main.py
external_repos/SJTU-DMTai__qlib/qlib/contrib/meta/incremental/
external_repos/SJTU-DMTai__qlib/qlib/contrib/model/
```

Example commands from repo:

```bash
python -u main.py run_all --forecast_model GRU --market csi300 --data_dir crowd_data --rank_label False --naive True

python -u main.py run_all --forecast_model GRU --market csi300 --data_dir crowd_data --rank_label False \
  --num_head 8 --tau 10 --lr 0.001 --lr_da 0.01 \
  --online_lr "{'lr': 0.001, 'lr_da': 0.0001, 'lr_ma': 0.001}"
```

## Reproduction Risks

- Requires the SJTU fork and additional package `higher`.
- Needs a complete Qlib runtime and likely PyTorch.
- Requires longer rolling/incremental windows; smoke data is insufficient.
- Default implementation can use substantial RAM/GPU memory.
- Hyperparameter tuning for `lr`, `lr_da`, and `lr_ma` is necessary.
- The README says paper settings are not necessarily optimal for practical deployment.


```

## repo_analysis.md

```text
# DoubleAdapt Repository Analysis

## Repository

`SJTU-DMTai/qlib`

## Status

Cloned locally at:

```text
external_repos/SJTU-DMTai__qlib
```

## Notes

- README identifies this directory as official DoubleAdapt implementation.
- Core framework is under `qlib/contrib/meta/incremental/`.
- The method has heavier online/incremental workflow requirements than TRA and MASTER.


```

## reproduction_plan.md

```text
# DoubleAdapt Reproduction Plan

## Local Code Entrypoints

```text
external_repos/SJTU-DMTai__qlib/examples/benchmarks_dynamic/incremental/
external_repos/SJTU-DMTai__qlib/qlib/contrib/meta/incremental/
```

## China A-Share Adaptation

1. Build the static CSI300 dataset first.
2. Add rolling/incremental split definitions after baseline results exist.
3. Start from the fork's incremental README commands.
4. Use monthly retraining plus 2-3 trading day adaptation as a candidate practical setting.
5. Compare against rolling retraining baseline.

## Expected Outputs

- Offline baseline result.
- Online/incremental adaptation result.
- Concept drift period analysis for China A shares.


```

## configs/china_a_share_smoke.json

```text
{
  "paper_id": "2023_doubleadapt_zhao",
  "model": "DoubleAdapt",
  "task": "trend_prediction_dynamic_adaptation",
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
    "repo": "Stock_benchmark/external_repos/SJTU-DMTai__qlib",
    "workflow_dir": "examples/benchmarks_dynamic/incremental",
    "meta_module_dir": "qlib/contrib/meta/incremental"
  },
  "first_target": {
    "base_model": "GRU",
    "adaptation_mode": "incremental rolling smoke after static baseline",
    "formal_split": "monthly train/update/test windows after long-history data is available"
  },
  "blocked_by": [
    "Full fork-compatible pyqlib runtime is unavailable.",
    "DoubleAdapt requires long rolling windows; the current smoke sample is too short for a meaningful adaptation run."
  ]
}

```

## configs/china_a_share_formal.json

```text
{
  "paper_id": "2023_doubleadapt_zhao",
  "model": "DoubleAdapt",
  "task": "trend_prediction_dynamic_adaptation",
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
    "mode": "doubleadapt",
    "lookback": 20,
    "max_train_rows": 50000,
    "outputs": {
      "h1": "Stock_benchmark/experiments/paper_runs/doubleadapt_formal_csi300_2018_2024_h1.csv",
      "h5": "Stock_benchmark/experiments/paper_runs/doubleadapt_formal_csi300_2018_2024_h5.csv"
    }
  },
  "official_runtime_status": "Blocked until PyTorch/fork-compatible Qlib runtime is provisioned."
}

```

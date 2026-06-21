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


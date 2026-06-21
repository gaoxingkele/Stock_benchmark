# Method and Engineering Notes

## Paper digest

Stock trend forecasting is a fundamental task of quantitative invest- ment where precise predictions of price trends are indispensable. As an online service, stock data continuously arrive over time. It is practical and efficient to incrementally update the forecast model with the latest data which may reveal some new patterns recurring in the future stock market. However, incremental learning for stock trend forecasting still remains under-explored due to the challenge of distribution shifts (a.k.a. concept drifts). With the stock market dynamically evolving, the distribution of future data can slightly or significantly differ from incremental data, hindering the effective- ness of incremental updates. To address this challenge, we propose DoubleAdapt, an end-to-end framework with two adapters, which can effectively adapt the data and the model to mitigate the effects of distribution shifts. Our key insight is to automatically learn how to adapt stock data into a locally stationary distribution in favor of profitable updates. Complemented by data adaptation, we can con- fidently adapt the model parameters under mitigated distribution shifts. We cast each incremental learning task as a meta-learning task and automatically optimize the adapters for desirable data adaptation and parameter initialization. Experiments on real-world stock datasets demonstrate that DoubleAdapt achieves state-of-the- art predictive performance and shows considerable efficiency. Our code is available at https://github.com/SJTU-Quant/qlib/. CCS CONCEPTS • Computing methodologies→ Online learning settings; • In- formation systems→ Data stream mining. KEYWORDS Stock trend forecasting; Incremental learning; Distribution shift ACM Reference Format: Lifan Zhao, Shuming Kong, and Yanyan Shen. 2023. DoubleAdapt: A Meta- learning Approach to Incremental Learning for Stock Trend Forecasting. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD ’23), August 6–10

## Local project notes

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

# Method and Engineering Notes

## Paper digest

Successful quantitative investment usually relies on precise pre- dictions of the future movement of the stock price. Recently, ma- chine learning based solutions have shown their capacity to give more accurate stock prediction and become indispensable compo- nents in modern quantitative investment systems. However, the i.i.d. assumption behind existing methods is inconsistent with the existence of diverse trading patterns1 in the stock market, which inevitably limits their ability to achieve better stock prediction performance. In this paper, we propose a novel architecture, Tem- poral Routing Adaptor (TRA), to empower existing stock prediction models with the ability to model multiple stock trading patterns. Essentially, TRA is a lightweight module that consists of a set of independent predictors for learning multiple patterns as well as a router to dispatch samples to different predictors. Nevertheless, the lack of explicit pattern identifiers makes it quite challenging to train an effective TRA-based model. To tackle this challenge, we further design a learning algorithm based on Optimal Transport (OT) to obtain the optimal sample to predictor assignment and effectively optimize the router with such assignment through an auxiliary loss term. Experiments on the real-world stock ranking task show that compared to the state-of-the-art baselines, e.g., Attention LSTM and Transformer, the proposed method can improve information coefficient (IC) from 0.053 to 0.059 and 0.051 to 0.056 respectively. Our dataset and code used in this work are publicly available2. ∗The first two authors have equal contribution. †This work was done when the first author was an intern at Microsoft Research Asia. 1In this paper, a trading pattern means the causal relation between the available information at the current time (i.e., feature) and the stock price movement in the future (i.e., label). 2https://github.com/microsoft/qlib/tree/main/examples/benchmarks/TRA Permission to make digital

## Local project notes

## README.md

```text
# 2021 TRA Lin

## Paper

- Title: Learning Multiple Stock Trading Patterns with Temporal Routing Adaptor and Optimal Transport
- Authors: Hengxu Lin; Dong Zhou; Weiqing Liu; Jiang Bian
- Year: 2021
- Venue: KDD 2021
- PDF: https://arxiv.org/abs/2106.12950
- Local PDF: `papers/raw/2021_tra_lin.pdf`
- Code: `external_repos/microsoft__qlib/examples/benchmarks/TRA`

## Benchmark Role

Core CCF-A stock-specific model. Use as the first paper reproduction after LightGBM validates the China A-share data loop.

## Status

- PDF downloaded and header verified.
- Code repository cloned through `microsoft/qlib`.

```

## notes.md

```text
# TRA Notes

## Core Problem

TRA targets stock ranking prediction under non-stationary market conditions. The paper argues that the usual i.i.d. assumption is weak for stock data because different trading patterns can coexist and recur over time.

## Method

Temporal Routing Adaptor is a plug-in module for existing sequence models such as ALSTM and Transformer.

Core components:

- Multiple linear predictors represent different latent trading patterns.
- A router assigns each sample to a predictor.
- The router uses both backbone latent representation and historical prediction-error memory.
- Optimal Transport regularization prevents trivial routing where nearly all samples go to one predictor.
- Sinkhorn is used to solve the sample-to-predictor assignment problem.

Important implementation detail:

- TRA needs temporal prediction error memory, so test/inference must respect chronological order.
- The old paper reproduction path used pretraining configs before TRA configs.
- The maintained Qlib path exposes `TRAModel` through workflow YAML.

## Data

Paper setting:

- China stock market.
- CSI800 stocks.
- Source: baostock.
- 16 hand-crafted features including valuation, growth, momentum, reversal, and range features.

Project adaptation:

- Use Tushare instead of baostock.
- Start with CSI300, then expand to CSI800/CSI500-compatible universe if needed.
- Initial shared features: Qlib Alpha158/Alpha360 or the local OHLCV/basic panel until full Qlib environment is ready.

## Labels

Paper:

- Stock ranking prediction.
- Labels are percentiles of cross-sectional returns at the end of next month.
- Percentile labels reduce sensitivity to outlier raw returns and improve comparability across market states.

Qlib config:

- Qlib TRA workflow configs use Alpha158/Alpha360 handlers.
- The maintained benchmark can use Qlib label expressions and processors.

Project adaptation:

- First smoke label: 1-day forward return.
- Formal reproduction label: 5-day and monthly cross-sectional rank labels.
- Use `CSRankNorm` for rank experiments.

## Metrics

Paper reports:

- MSE
- MAE
- IC
- ICIR
- Annualized return
- Annualized volatility
- Sharpe ratio
- Max drawdown

Project first metrics:

- IC
- RankIC
- ICIR
- RankICIR
- Annualized return
- Information ratio
- Max drawdown
- Turnover

## Baselines

Paper compares against:

- Linear
- LightGBM
- MLP
- SFM
- ALSTM
- Transformer
- ALSTM + temporal smoothing variants
- Transformer + temporal smoothing variants

Project first baseline chain:

1. Local LightGBM smoke baseline.
2. Formal Qlib LightGBM after Qlib runtime is fixed.
3. ALSTM/Transformer.
4. ALSTM+TRA or Transformer+TRA.

## Code Entrypoints

```text
external_repos/microsoft__qlib/examples/benchmarks/TRA/
external_repos/microsoft__qlib/examples/benchmarks/TRA/workflow_config_tra_Alpha360.yaml
external_repos/microsoft__qlib/examples/benchmarks/TRA/workflow_config_tra_Alpha158.yaml
external_repos/microsoft__qlib/qlib/contrib/model/pytorch_tra.py
```

## Reproduction Risks

- Full Qlib runtime currently blocked by missing compiled extension until MSVC Build Tools or a better Python environment is available.
- TRA requires sequence data and prediction-error memory, so a tiny smoke dataset is not meaningful for model quality.
- Paper uses CSI800 and monthly rank labels; current project smoke data uses 5 CSI300 stocks and daily labels.
- Sinkhorn epsilon is scale-sensitive; Qlib README warns NaN loss can occur if epsilon is poorly matched to input scale.


```

## repo_analysis.md

```text
# TRA Repository Analysis

## Repository

`microsoft/qlib`

## Status

Cloned locally at:

```text
external_repos/microsoft__qlib
```

## Notes

- TRA is integrated into Qlib workflow configs.
- It requires a time-series dataset handler and historical prediction errors for routing.
- The README notes an init/pretraining stage for backbone models in older configs.


```

## reproduction_plan.md

```text
# TRA Reproduction Plan

## Local Code Entrypoints

```text
external_repos/microsoft__qlib/examples/benchmarks/TRA/
external_repos/microsoft__qlib/qlib/contrib/model/pytorch_tra.py
```

First config:

```text
examples/benchmarks/TRA/workflow_config_tra_Alpha360.yaml
```

## China A-Share Adaptation

1. Run Qlib LightGBM on CSI300 first to validate the dataset.
2. Use Alpha360 initially because Qlib has a standard TRA config for it.
3. Replace default Qlib data path with `data/processed/cn_a_share/qlib`.
4. Start with 1-day return ranking label, then add 5-day label.
5. Compare against ALSTM/Transformer backbone where feasible.

## Expected Outputs

- IC, ICIR, RankIC, RankICIR.
- Top-k/dropout portfolio report.
- Runtime and GPU/CPU memory notes.


```

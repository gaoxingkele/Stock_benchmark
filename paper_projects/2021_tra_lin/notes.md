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


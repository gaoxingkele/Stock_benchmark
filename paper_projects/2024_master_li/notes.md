# MASTER Notes

## Core Problem

MASTER addresses stock price forecasting with complex stock correlations. It argues that existing methods mostly mix temporal representations at aligned timestamps, while real stock influence can be momentary and cross-time.

## Method

MASTER stands for Market-Guided Stock Transformer.

Main components:

- Market-guided gating: builds a market status vector and uses it to rescale feature dimensions.
- Intra-stock aggregation: attention along each stock's historical sequence.
- Inter-stock aggregation: attention among stocks at each time step.
- Temporal aggregation: combines resulting time representations for final prediction.

The architecture alternates intra-stock and inter-stock aggregation to reduce attention complexity compared with directly attending over the full stock-time field.

## Data

Paper setting:

- Chinese stock market.
- CSI300 and CSI800.
- Daily data from 2008 to 2022.
- Train: Q1 2008 to Q1 2020.
- Validation: Q2 2020.
- Test: Q3 2020 to Q4 2022.
- Alpha158 features.
- Lookback window `tau = 8`.
- Prediction interval `d = 5`.

Market representation:

- 63 features using CSI300, CSI500, and CSI800 market indices.
- Reference intervals `d' = 5, 10, 20, 30, 60`.

Project adaptation:

- Start with CSI300 and the CSI300 index.
- Add CSI500/CSI800 index features after raw index data is in place.
- Use Tushare `index_daily` and local feature generation for market representation if Qlib Alpha158 is not available.

## Labels

Paper:

- Predicts future normalized return ratio.
- Qlib config uses `Ref($close, -5) / Ref($close, -1) - 1`.
- Qlib learn processor uses `CSRankNorm`.

Project adaptation:

- First formal config should use 5-day forward return with cross-sectional ranking.
- Smoke experiments already use 1-day return but are not a MASTER-quality test.

## Metrics

Expected shared metrics:

- IC
- RankIC
- ICIR
- RankICIR
- Portfolio return metrics through Qlib `TopkDropoutStrategy`

## Baselines

Paper compares with:

- XGBoost
- LSTM
- GRU
- TCN
- Transformer
- HIST
- DTML
- Other stock forecasting baselines

Project comparison:

1. LightGBM/Qlib baseline.
2. Transformer.
3. TRA.
4. MASTER.

## Code Entrypoints

```text
external_repos/SJTU-DMTai__qlib/examples/benchmarks/MASTER/
external_repos/SJTU-DMTai__qlib/examples/benchmarks/MASTER/workflow_config_master_Alpha158.yaml
external_repos/SJTU-DMTai__qlib/qlib/contrib/model/pytorch_master_ts.py
external_repos/SJTU-DMTai__qlib/qlib/contrib/data/dataset.py
```

## Reproduction Risks

- MASTER depends on fork-specific Qlib modifications.
- It needs a proper market data handler in addition to the stock data handler.
- The paper uses long historical data from 2008 onward; short smoke windows cannot exercise the model.
- Full run likely needs GPU/PyTorch and a complete Qlib environment.
- Need to confirm how `CSI800` market representation maps to available Tushare indices or construct a proxy.


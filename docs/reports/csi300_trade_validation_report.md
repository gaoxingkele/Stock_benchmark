# CSI300 Trading Validation Report

This report validates the strongest directions from the 24-paper original-vs-China comparison on CSI300 2018-2024 using H5 paper-inspired proxy scores.

## Protocol

- Universe: processed CSI300 A-share panel, test period 2023-01-03 to 2024-12-31.
- Signal horizon: H5 scores; portfolio return is the selected 5-day forward return divided by 5 to approximate daily overlapping holding returns.
- Portfolio: daily rebalanced equal-weight Top30 long-only basket.
- Cost: 10 bps one-way cost applied to daily turnover.
- Checks: net annual return, Sharpe, max drawdown, turnover, yearly stability, industry concentration, size exposure, and an industry/size-neutral score variant.
- Important limitation: these are paper-inspired NumPy proxy mechanisms, not full official reproductions for every paper.

## Candidate Selection

The top H5 IC/RankIC papers were RD-Agent-Quant, DiffsFormer, DoubleAdapt, and DoubleEnsemble. They share the same DoubleAdapt-family proxy mechanism in the current runnable benchmark, so Master, TCTS, HIST, and TRA proxy mechanisms are included as controls.

## Main Results

| Model | Proxy mode | Variant | Ann. Return | Sharpe | MDD | Cum. Return | Avg Turnover | Max Industry Wt | Size Exposure | Yearly Ann. Returns |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| rd_agent_quant | doubleadapt | raw | 43.90% | 3.05 | -13.68% | 99.74% | 10.91% | 18.87% | 0.005 | 2023:0.3822;2024:0.4995 |
| rd_agent_quant | doubleadapt | industry_size_neutral | 32.77% | 2.42 | -19.27% | 71.39% | 11.23% | 14.62% | -0.149 | 2023:0.2318;2024:0.4333 |
| diffsformer | doubleadapt | raw | 43.90% | 3.05 | -13.68% | 99.74% | 10.91% | 18.87% | 0.005 | 2023:0.3822;2024:0.4995 |
| diffsformer | doubleadapt | industry_size_neutral | 32.77% | 2.42 | -19.27% | 71.39% | 11.23% | 14.62% | -0.149 | 2023:0.2318;2024:0.4333 |
| doubleadapt | doubleadapt | raw | 43.90% | 3.05 | -13.68% | 99.74% | 10.91% | 18.87% | 0.005 | 2023:0.3822;2024:0.4995 |
| doubleadapt | doubleadapt | industry_size_neutral | 32.77% | 2.42 | -19.27% | 71.39% | 11.23% | 14.62% | -0.149 | 2023:0.2318;2024:0.4333 |
| doubleensemble | doubleadapt | raw | 43.90% | 3.05 | -13.68% | 99.74% | 10.91% | 18.87% | 0.005 | 2023:0.3822;2024:0.4995 |
| doubleensemble | doubleadapt | industry_size_neutral | 32.77% | 2.42 | -19.27% | 71.39% | 11.23% | 14.62% | -0.149 | 2023:0.2318;2024:0.4333 |
| alphaprobe | master | raw | -7.80% | -0.61 | -42.84% | -14.30% | 51.21% | 17.18% | -0.217 | 2023:-0.1831;2024:0.0433 |
| alphaprobe | master | industry_size_neutral | -6.39% | -0.62 | -35.47% | -11.80% | 46.42% | 14.79% | 0.249 | 2023:-0.2301;2024:0.1427 |
| master | master | raw | -7.80% | -0.61 | -42.84% | -14.30% | 51.21% | 17.18% | -0.217 | 2023:-0.1831;2024:0.0433 |
| master | master | industry_size_neutral | -6.39% | -0.62 | -35.47% | -11.80% | 46.42% | 14.79% | 0.249 | 2023:-0.2301;2024:0.1427 |
| tcts | tcts | raw | -10.93% | -0.83 | -44.52% | -19.74% | 68.61% | 13.97% | -0.200 | 2023:-0.1988;2024:-0.0074 |
| tcts | tcts | industry_size_neutral | -9.51% | -0.84 | -39.54% | -17.29% | 67.14% | 11.89% | 0.127 | 2023:-0.2050;2024:0.0328 |
| hist | hist | raw | -2.97% | -0.23 | -40.24% | -5.57% | 39.90% | 17.11% | -0.242 | 2023:-0.1350;2024:0.0910 |
| hist | hist | industry_size_neutral | -2.81% | -0.29 | -31.17% | -5.28% | 36.12% | 17.04% | 0.269 | 2023:-0.1869;2024:0.1660 |
| tra | tra | raw | -2.94% | -0.21 | -43.04% | -5.51% | 45.46% | 16.80% | -0.300 | 2023:-0.1433;2024:0.1026 |
| tra | tra | industry_size_neutral | -9.96% | -0.88 | -41.80% | -18.07% | 44.15% | 14.36% | 0.070 | 2023:-0.1955;2024:0.0102 |

## Unique Mechanism Ranking

| Proxy mode | Representative paper | Net Ann. Return | Sharpe | MDD | Decision |
|---|---|---:|---:|---:|---|
| doubleadapt | rd_agent_quant | 43.90% | 3.05 | -13.68% | pass research-to-trade screen |
| tra | tra | -2.94% | -0.21 | -43.04% | reject for now |
| hist | hist | -2.97% | -0.23 | -40.24% | reject for now |
| master | alphaprobe | -7.80% | -0.61 | -42.84% | reject for now |
| tcts | tcts | -10.93% | -0.83 | -44.52% | reject for now |

## Interpretation

- DoubleAdapt-family is the only direction that currently has practical trading research value. It remains positive after 10 bps turnover cost, with raw net annual return 43.90%, Sharpe 3.05, MDD -13.68%, and both 2023/2024 positive.
- The industry/size-neutral residual version is weaker but still positive: annual return 32.77%, Sharpe 2.42, MDD -19.27%, and both years positive. This reduces the chance that the result is only a sector or size exposure.
- Master/AlphaPROBE, TCTS, HIST, and TRA proxy modes do not pass the trading screen. They are negative after costs and have large drawdowns around -31% to -45%.
- Turnover is manageable for DoubleAdapt-family at about 10.9% per day. The rejected modes have much higher turnover, especially TCTS and Master, making costs more damaging.
- The top four papers are not independent signals in this implementation: RD-Agent-Quant, DiffsFormer, DoubleAdapt, and DoubleEnsemble all route to the same DoubleAdapt-style proxy. Treat them as one candidate family, not four diversified strategies.

## Trading Guidance

Current evidence supports advancing DoubleAdapt-family to the next validation stage, but not direct live trading yet.

Required before live use:

1. Add suspension, limit-up/down, liquidity, and realistic execution filters.
2. Replace proxy scores with at least one full implementation for DoubleAdapt/RD-Agent/DiffsFormer, or prove the proxy is sufficiently faithful.
3. Test Top10/Top30/Top50, weekly rebalance, and 5/10/20 bps cost sensitivity.
4. Run walk-forward retraining beyond the current 2023-2024 test split and check factor decay by month.
5. Confirm no label leakage from overlapping H5 return construction before promoting to paper trading.

Bottom line: use DoubleAdapt-family as the only actionable research direction from this batch; do not use the other proxy modes for trading without substantial redesign.

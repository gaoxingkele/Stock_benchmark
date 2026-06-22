# Expansion-Only Paper Candidate Validation Against Best Proxy

Date: 2026-06-22

This report validates the seven previously experiment-missing expansion papers against the current best local proxy, `rd_agent_quant / DoubleAdapt-family`, on China A-share, US large-cap, and HK large-cap markets.

Important scope note: these are paper-inspired engineering proxies, not official reproductions of every paper. The goal is to bind each paper direction to a runnable, comparable local protocol before deciding which papers deserve full ARA compilation or official-code reproduction.

Per-stock score dumps are intentionally not committed because they are large and fully regenerable from the commands below. The repository keeps the script, daily backtest files, and summary CSVs.

## Protocol

| Item | Setting |
|---|---|
| Label | H5 forward return |
| Portfolio | equal-weight long-only Top30 |
| Rebalance | daily |
| Cost | single-side 10 bps |
| Train | 2018-01-02 to 2021-12-31 |
| Valid | 2022 calendar year |
| Test | 2023-01-03 to 2025-12-31 |
| Variants | raw and industry/size neutralized |

## Paper Proxy Mapping

| Paper ID | Local validation proxy |
|---|---|
| `2020_qlib_yang` | Alpha158-style OHLCV/value ridge proxy |
| `2025_alphaagent_tang` | regularized formula-alpha selection: mom_60,alpha_value_mom,alpha_quality_liquidity,alpha_price_volume,ma_gap_20,rev_5,volume_z_20,mom_20 |
| `2025_cogalpha_liu` | code-generated formula feature ridge: mom_60,alpha_value_mom,alpha_quality_liquidity,alpha_price_volume,rsi_14,macd_proxy,rev_5,volume_z_20,tin_boll_mom,vol_20,price_range |
| `2025_quantbench_wang` | QuantBench-style Alpha/indicator/time-series ensemble proxy |
| `2025_fintsb` | financial time-series momentum/volatility benchmark proxy |
| `2024_technical_indicator_impact` | TA-Lib-style indicator ridge proxy |
| `2025_tin` | technical indicator interaction network proxy |

## Market-Level Best Candidate Vs Best Proxy

| Market | Variant | Best expansion candidate | Candidate ann. | Candidate Sharpe | Best proxy ann. | Best proxy Sharpe | Ann. delta |
|---|---|---|---:|---:|---:|---:|---:|
| China A-share CSI300 | raw | `2025_fintsb` | 10.42% | 0.74 | 60.06% | 4.30 | -49.63% |
| China A-share CSI300 | industry_size_neutral | `2025_fintsb` | 10.17% | 0.78 | 47.56% | 3.66 | -37.40% |
| US large cap | raw | `2020_qlib_yang` | 31.86% | 4.92 | 32.61% | 5.24 | -0.74% |
| US large cap | industry_size_neutral | `2020_qlib_yang` | 31.86% | 4.92 | 31.26% | 5.17 | +0.60% |
| HK large cap | raw | `2020_qlib_yang` | 11.89% | 1.23 | 22.59% | 2.17 | -10.70% |
| HK large cap | industry_size_neutral | `2020_qlib_yang` | 11.89% | 1.23 | 17.53% | 1.75 | -5.64% |

## China A-share CSI300

| Method | Variant | Ann. return | Sharpe | MDD | Cum. return | Ann. delta vs best proxy |
|---|---|---:|---:|---:|---:|---:|
| `2025_fintsb` | industry_size_neutral | 10.17% | 0.78 | -31.80% | 32.22% | -37.40% |
| `2025_tin` | industry_size_neutral | 7.97% | 0.67 | -32.68% | 24.78% | -39.59% |
| `2025_quantbench_wang` | industry_size_neutral | 6.63% | 0.53 | -34.55% | 20.35% | -40.93% |
| `2025_alphaagent_tang` | industry_size_neutral | 6.05% | 0.49 | -36.43% | 18.46% | -41.52% |
| `2020_qlib_yang` | industry_size_neutral | 5.47% | 0.47 | -32.43% | 16.60% | -42.09% |
| `2025_cogalpha_liu` | industry_size_neutral | 5.22% | 0.41 | -35.64% | 15.80% | -42.35% |
| `2024_technical_indicator_impact` | industry_size_neutral | -0.50% | -0.04 | -38.78% | -1.45% | -48.07% |
| `2025_fintsb` | raw | 10.42% | 0.74 | -34.31% | 33.12% | -49.63% |
| `2025_tin` | raw | 7.50% | 0.57 | -36.51% | 23.20% | -52.56% |
| `2025_quantbench_wang` | raw | 4.45% | 0.31 | -43.48% | 13.38% | -55.61% |
| `2025_alphaagent_tang` | raw | 1.68% | 0.15 | -28.75% | 4.91% | -58.38% |
| `2024_technical_indicator_impact` | raw | 0.66% | 0.05 | -43.44% | 1.90% | -59.40% |
| `2020_qlib_yang` | raw | -0.33% | -0.02 | -43.60% | -0.94% | -60.38% |
| `2025_cogalpha_liu` | raw | -2.27% | -0.16 | -45.83% | -6.41% | -62.33% |

## US large cap

| Method | Variant | Ann. return | Sharpe | MDD | Cum. return | Ann. delta vs best proxy |
|---|---|---:|---:|---:|---:|---:|
| `2020_qlib_yang` | industry_size_neutral | 31.86% | 4.92 | -15.18% | 128.28% | +0.60% |
| `2025_fintsb` | industry_size_neutral | 26.59% | 4.30 | -14.42% | 102.12% | -4.67% |
| `2025_quantbench_wang` | industry_size_neutral | 25.93% | 4.19 | -14.69% | 98.99% | -5.33% |
| `2024_technical_indicator_impact` | industry_size_neutral | 25.69% | 4.16 | -14.30% | 97.85% | -5.57% |
| `2025_alphaagent_tang` | industry_size_neutral | 24.82% | 4.12 | -14.54% | 93.78% | -6.45% |
| `2025_tin` | industry_size_neutral | 24.10% | 3.95 | -14.19% | 90.46% | -7.17% |
| `2025_cogalpha_liu` | industry_size_neutral | 23.05% | 3.80 | -13.97% | 85.70% | -8.21% |
| `2020_qlib_yang` | raw | 31.86% | 4.92 | -15.18% | 128.28% | -0.74% |
| `2025_fintsb` | raw | 30.78% | 4.64 | -15.79% | 122.71% | -1.83% |
| `2025_quantbench_wang` | raw | 29.72% | 4.44 | -15.79% | 117.39% | -2.89% |
| `2025_tin` | raw | 28.34% | 4.33 | -15.43% | 110.57% | -4.27% |
| `2024_technical_indicator_impact` | raw | 28.05% | 4.21 | -15.61% | 109.12% | -4.56% |
| `2025_alphaagent_tang` | raw | 24.45% | 3.96 | -14.76% | 92.10% | -8.15% |
| `2025_cogalpha_liu` | raw | 24.30% | 3.77 | -14.79% | 91.39% | -8.31% |

## HK large cap

| Method | Variant | Ann. return | Sharpe | MDD | Cum. return | Ann. delta vs best proxy |
|---|---|---:|---:|---:|---:|---:|
| `2020_qlib_yang` | industry_size_neutral | 11.89% | 1.23 | -24.21% | 38.78% | -5.64% |
| `2024_technical_indicator_impact` | industry_size_neutral | 11.63% | 1.10 | -28.66% | 37.84% | -5.90% |
| `2025_quantbench_wang` | industry_size_neutral | 10.46% | 0.98 | -28.88% | 33.65% | -7.08% |
| `2025_tin` | industry_size_neutral | 9.30% | 0.89 | -27.77% | 29.62% | -8.23% |
| `2025_cogalpha_liu` | industry_size_neutral | 9.21% | 0.87 | -28.61% | 29.29% | -8.33% |
| `2025_fintsb` | industry_size_neutral | 8.71% | 0.82 | -29.39% | 27.58% | -8.82% |
| `2025_alphaagent_tang` | industry_size_neutral | 8.18% | 0.79 | -27.68% | 25.78% | -9.35% |
| `2020_qlib_yang` | raw | 11.89% | 1.23 | -24.21% | 38.78% | -10.70% |
| `2024_technical_indicator_impact` | raw | 10.46% | 0.93 | -29.18% | 33.68% | -12.13% |
| `2025_alphaagent_tang` | raw | 9.60% | 0.87 | -29.51% | 30.66% | -12.99% |
| `2025_quantbench_wang` | raw | 8.65% | 0.76 | -31.15% | 27.38% | -13.94% |
| `2025_cogalpha_liu` | raw | 8.53% | 0.78 | -29.78% | 26.97% | -14.06% |
| `2025_tin` | raw | 8.36% | 0.75 | -30.19% | 26.40% | -14.23% |
| `2025_fintsb` | raw | 7.27% | 0.65 | -32.14% | 22.72% | -15.32% |

## Conclusion

1. None of the seven expansion-only candidates beats the current `rd_agent_quant / DoubleAdapt-family` best proxy on the three-market 2023-2025 protocol.
2. US large cap is the closest case: `2020_qlib_yang` Alpha158-style proxy reaches 31.86% raw annualized return versus the best proxy at 32.61%, only -0.74 percentage points behind. This suggests Qlib-style hand-crafted factor infrastructure is a strong reproducible baseline for US large-cap data.
3. China A-share is the clearest gap: the best expansion candidate is `2025_fintsb` at 10.42% raw annualized return, far below the best proxy at 60.06%. Formula/indicator-only proxies do not explain the current best A-share result.
4. HK large cap remains difficult for the expansion candidates: the best candidate is `2020_qlib_yang` at 11.89% raw annualized return, below the best proxy at 22.59%.
5. TA-Lib/TIN-style indicators are useful but not sufficient as standalone methods. They are better treated as additional feature primitives for RD-Agent/AlphaAgent-style search than as replacements for DoubleAdapt-family adaptation.

## Updated Audit Status

- Previously experiment-missing expansion papers: 7.
- Now locally validated with runnable proxy experiments on China A-share, US large-cap, and HK large-cap: 7 / 7.
- Still missing full ARA engineering packages for these seven papers: 7 / 7.
- Next step should be ARA compilation for the most relevant subset: `2020_qlib_yang`, `2025_alphaagent_tang`, `2025_quantbench_wang`, `2024_technical_indicator_impact`, and `2025_tin`, with `2025_fintsb` kept as a benchmark reference.

## Reproduction

```powershell
python scripts\run_unvalidated_paper_candidates.py --panel data\processed\cn_a_share\csi300_2018_2026_ytd\panel.csv --stock-basic data\raw\tushare\csi300_2025_2026\stock_basic.csv --market cn_a_share --horizon 5 --topk 30 --cost-bps 10 --train-start 2018-01-02 --train-end 2021-12-31 --valid-start 2022-01-04 --valid-end 2022-12-30 --test-start 2023-01-03 --test-end 2025-12-31 --out-dir experiments\unvalidated_candidates\cn_a_share_2018_2026_ytd

python scripts\run_unvalidated_paper_candidates.py --panel data\processed\global_markets\us_large_cap_2018_2026\panel.csv --stock-basic data\processed\global_markets\us_large_cap_2018_2026\stock_basic.csv --market us_large_cap --horizon 5 --topk 30 --cost-bps 10 --train-start 2018-01-02 --train-end 2021-12-31 --valid-start 2022-01-03 --valid-end 2022-12-30 --test-start 2023-01-03 --test-end 2025-12-31 --out-dir experiments\unvalidated_candidates\us_large_cap_2018_2026

python scripts\run_unvalidated_paper_candidates.py --panel data\processed\global_markets\hk_large_cap_2018_2026\panel.csv --stock-basic data\processed\global_markets\hk_large_cap_2018_2026\stock_basic.csv --market hk_large_cap --horizon 5 --topk 30 --cost-bps 10 --train-start 2018-01-02 --train-end 2021-12-31 --valid-start 2022-01-03 --valid-end 2022-12-30 --test-start 2023-01-03 --test-end 2025-12-31 --out-dir experiments\unvalidated_candidates\hk_large_cap_2018_2026
```

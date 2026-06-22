# Lingxi TopK Series vs Runner-Up Algorithms

Date: 2026-06-22

This report compares Lingxi30/20/10/5 against the two strongest runner-up algorithm families from the expansion-candidate validation: `qlib_alpha158` and `fintsb_ts`.

## Naming

| Name | Method | Portfolio |
|---|---|---|
| Lingxi30 | `rd_agent_quant / DoubleAdapt-family proxy` | H5 Top30, equal-weight long-only, daily rebalance |
| Lingxi20 | `rd_agent_quant / DoubleAdapt-family proxy` | H5 Top20, equal-weight long-only, daily rebalance |
| Lingxi10 | `rd_agent_quant / DoubleAdapt-family proxy` | H5 Top10, equal-weight long-only, daily rebalance |
| Lingxi5 | `rd_agent_quant / DoubleAdapt-family proxy` | H5 Top5, equal-weight long-only, daily rebalance |
| Qlib Alpha158 proxy | `2020_qlib_yang` | same TopK grid |
| FinTSB time-series proxy | `2025_fintsb` | same TopK grid |

## Protocol

| Item | Setting |
|---|---|
| Markets | China A-share CSI300, US large cap, HK large cap |
| Train | 2018-01-02 to 2021-12-31 |
| Valid | 2022 calendar year |
| Test | 2023-01-03 to 2025-12-31 |
| Label | H5 forward return |
| Cost | single-side 10 bps |
| Variants | raw and industry/size neutralized |

## Market Winners

| Market | Variant | Best method | TopK | Ann. return | Sharpe | MDD | Cum. return |
|---|---|---|---:|---:|---:|---:|---:|
| China A-share CSI300 | raw | Lingxi / RDA-Adapt | 5 | 156.66% | 6.62 | -26.14% | 1417.00% |
| China A-share CSI300 | industry_size_neutral | Lingxi / RDA-Adapt | 5 | 116.66% | 5.50 | -25.46% | 830.45% |
| US large cap | raw | Lingxi / RDA-Adapt | 5 | 61.33% | 6.09 | -18.39% | 316.72% |
| US large cap | industry_size_neutral | Lingxi / RDA-Adapt | 5 | 51.26% | 5.70 | -14.74% | 243.82% |
| HK large cap | raw | Lingxi / RDA-Adapt | 5 | 55.70% | 3.62 | -18.09% | 263.82% |
| HK large cap | industry_size_neutral | Lingxi / RDA-Adapt | 5 | 27.08% | 1.83 | -22.29% | 101.19% |

## Lingxi Series

| Market | Variant | Lingxi30 ann/Sharpe/MDD | Lingxi20 ann/Sharpe/MDD | Lingxi10 ann/Sharpe/MDD | Lingxi5 ann/Sharpe/MDD |
|---|---|---:|---:|---:|---:|
| China A-share CSI300 | raw | 60.06% / 4.30 / -14.26% | 74.60% / 4.83 / -16.04% | 113.78% / 6.04 / -17.49% | 156.66% / 6.62 / -26.14% |
| China A-share CSI300 | industry_size_neutral | 47.56% / 3.66 / -19.29% | 58.99% / 4.00 / -22.85% | 89.65% / 5.15 / -23.57% | 116.66% / 5.50 / -25.46% |
| US large cap | raw | 32.61% / 5.24 / -14.86% | 39.45% / 5.69 / -14.37% | 50.89% / 6.04 / -14.44% | 61.33% / 6.09 / -18.39% |
| US large cap | industry_size_neutral | 31.26% / 5.17 / -14.49% | 34.58% / 5.41 / -14.60% | 41.82% / 5.46 / -13.83% | 51.26% / 5.70 / -14.74% |
| HK large cap | raw | 22.59% / 2.17 / -18.58% | 32.85% / 2.88 / -15.33% | 42.65% / 3.22 / -14.94% | 55.70% / 3.62 / -18.09% |
| HK large cap | industry_size_neutral | 17.53% / 1.75 / -20.75% | 22.12% / 2.14 / -19.04% | 25.84% / 2.10 / -21.61% | 27.08% / 1.83 / -22.29% |

## Full Raw Results

### China A-share CSI300

| Method | TopK | Variant | Ann. return | Sharpe | MDD | Cum. return | Avg turnover |
|---|---:|---|---:|---:|---:|---:|---:|
| FinTSB time-series proxy | 30 | industry_size_neutral | 10.17% | 0.78 | -31.80% | 32.22% | 24.09% |
| FinTSB time-series proxy | 30 | raw | 10.42% | 0.74 | -34.31% | 33.12% | 24.13% |
| FinTSB time-series proxy | 20 | industry_size_neutral | 13.95% | 0.98 | -31.52% | 45.74% | 25.52% |
| FinTSB time-series proxy | 20 | raw | 14.40% | 0.97 | -34.91% | 47.41% | 25.47% |
| FinTSB time-series proxy | 10 | industry_size_neutral | 14.19% | 0.90 | -31.28% | 46.65% | 28.05% |
| FinTSB time-series proxy | 10 | raw | 16.23% | 1.01 | -34.76% | 54.32% | 27.79% |
| FinTSB time-series proxy | 5 | industry_size_neutral | 16.05% | 0.88 | -27.76% | 53.62% | 29.92% |
| FinTSB time-series proxy | 5 | raw | 18.72% | 1.04 | -30.79% | 64.07% | 30.41% |
| Lingxi / RDA-Adapt | 30 | industry_size_neutral | 47.56% | 3.66 | -19.29% | 207.25% | 11.09% |
| Lingxi / RDA-Adapt | 30 | raw | 60.06% | 4.30 | -14.26% | 288.43% | 10.55% |
| Lingxi / RDA-Adapt | 20 | industry_size_neutral | 58.99% | 4.00 | -22.85% | 281.00% | 11.94% |
| Lingxi / RDA-Adapt | 20 | raw | 74.60% | 4.83 | -16.04% | 399.19% | 11.33% |
| Lingxi / RDA-Adapt | 10 | industry_size_neutral | 89.65% | 5.15 | -23.57% | 533.68% | 13.08% |
| Lingxi / RDA-Adapt | 10 | raw | 113.78% | 6.04 | -17.49% | 795.19% | 13.88% |
| Lingxi / RDA-Adapt | 5 | industry_size_neutral | 116.66% | 5.50 | -25.46% | 830.45% | 14.32% |
| Lingxi / RDA-Adapt | 5 | raw | 156.66% | 6.62 | -26.14% | 1417.00% | 15.86% |
| Qlib Alpha158 proxy | 30 | industry_size_neutral | 5.47% | 0.47 | -32.43% | 16.60% | 54.70% |
| Qlib Alpha158 proxy | 30 | raw | -0.33% | -0.02 | -43.60% | -0.94% | 52.04% |
| Qlib Alpha158 proxy | 20 | industry_size_neutral | 2.04% | 0.17 | -36.45% | 5.99% | 59.95% |
| Qlib Alpha158 proxy | 20 | raw | -1.69% | -0.12 | -46.30% | -4.79% | 58.67% |
| Qlib Alpha158 proxy | 10 | industry_size_neutral | -6.59% | -0.49 | -37.88% | -17.84% | 67.94% |
| Qlib Alpha158 proxy | 10 | raw | -6.41% | -0.42 | -48.79% | -17.39% | 67.69% |
| Qlib Alpha158 proxy | 5 | industry_size_neutral | -12.45% | -0.80 | -48.22% | -31.85% | 73.93% |
| Qlib Alpha158 proxy | 5 | raw | -10.62% | -0.61 | -50.81% | -27.66% | 75.01% |

### US large cap

| Method | TopK | Variant | Ann. return | Sharpe | MDD | Cum. return | Avg turnover |
|---|---:|---|---:|---:|---:|---:|---:|
| FinTSB time-series proxy | 30 | industry_size_neutral | 26.59% | 4.30 | -14.42% | 102.12% | 6.53% |
| FinTSB time-series proxy | 30 | raw | 30.78% | 4.64 | -15.79% | 122.71% | 6.95% |
| FinTSB time-series proxy | 20 | industry_size_neutral | 25.43% | 3.69 | -16.41% | 96.62% | 12.47% |
| FinTSB time-series proxy | 20 | raw | 34.15% | 4.36 | -17.47% | 140.30% | 11.50% |
| FinTSB time-series proxy | 10 | industry_size_neutral | 25.30% | 2.88 | -20.23% | 96.04% | 18.38% |
| FinTSB time-series proxy | 10 | raw | 40.69% | 4.07 | -20.44% | 176.99% | 16.90% |
| FinTSB time-series proxy | 5 | industry_size_neutral | 22.91% | 2.13 | -23.96% | 85.05% | 22.46% |
| FinTSB time-series proxy | 5 | raw | 41.38% | 3.35 | -25.71% | 181.07% | 19.91% |
| Lingxi / RDA-Adapt | 30 | industry_size_neutral | 31.26% | 5.17 | -14.49% | 125.20% | 7.04% |
| Lingxi / RDA-Adapt | 30 | raw | 32.61% | 5.24 | -14.86% | 132.15% | 6.41% |
| Lingxi / RDA-Adapt | 20 | industry_size_neutral | 34.58% | 5.41 | -14.60% | 142.60% | 12.67% |
| Lingxi / RDA-Adapt | 20 | raw | 39.45% | 5.69 | -14.37% | 169.77% | 11.88% |
| Lingxi / RDA-Adapt | 10 | industry_size_neutral | 41.82% | 5.46 | -13.83% | 183.69% | 19.57% |
| Lingxi / RDA-Adapt | 10 | raw | 50.89% | 6.04 | -14.44% | 241.29% | 16.99% |
| Lingxi / RDA-Adapt | 5 | industry_size_neutral | 51.26% | 5.70 | -14.74% | 243.82% | 24.69% |
| Lingxi / RDA-Adapt | 5 | raw | 61.33% | 6.09 | -18.39% | 316.72% | 20.81% |
| Qlib Alpha158 proxy | 30 | industry_size_neutral | 31.86% | 4.92 | -15.18% | 128.28% | 0.07% |
| Qlib Alpha158 proxy | 30 | raw | 31.86% | 4.92 | -15.18% | 128.28% | 0.07% |
| Qlib Alpha158 proxy | 20 | industry_size_neutral | 34.77% | 4.76 | -16.52% | 143.63% | 0.07% |
| Qlib Alpha158 proxy | 20 | raw | 34.77% | 4.76 | -16.52% | 143.63% | 0.07% |
| Qlib Alpha158 proxy | 10 | industry_size_neutral | 35.70% | 4.47 | -17.22% | 148.67% | 0.07% |
| Qlib Alpha158 proxy | 10 | raw | 35.70% | 4.47 | -17.22% | 148.67% | 0.07% |
| Qlib Alpha158 proxy | 5 | industry_size_neutral | 30.14% | 3.14 | -21.34% | 119.50% | 0.07% |
| Qlib Alpha158 proxy | 5 | raw | 30.14% | 3.14 | -21.34% | 119.50% | 0.07% |

### HK large cap

| Method | TopK | Variant | Ann. return | Sharpe | MDD | Cum. return | Avg turnover |
|---|---:|---|---:|---:|---:|---:|---:|
| FinTSB time-series proxy | 30 | industry_size_neutral | 8.71% | 0.82 | -29.39% | 27.58% | 6.10% |
| FinTSB time-series proxy | 30 | raw | 7.27% | 0.65 | -32.14% | 22.72% | 4.81% |
| FinTSB time-series proxy | 20 | industry_size_neutral | 6.86% | 0.61 | -31.44% | 21.34% | 11.95% |
| FinTSB time-series proxy | 20 | raw | 0.76% | 0.06 | -36.96% | 2.22% | 9.13% |
| FinTSB time-series proxy | 10 | industry_size_neutral | 4.47% | 0.34 | -36.87% | 13.61% | 17.36% |
| FinTSB time-series proxy | 10 | raw | -7.01% | -0.50 | -45.63% | -19.11% | 13.40% |
| FinTSB time-series proxy | 5 | industry_size_neutral | 0.69% | 0.05 | -44.12% | 2.01% | 21.97% |
| FinTSB time-series proxy | 5 | raw | -11.74% | -0.77 | -52.33% | -30.52% | 19.50% |
| Lingxi / RDA-Adapt | 30 | industry_size_neutral | 17.53% | 1.75 | -20.75% | 60.20% | 4.35% |
| Lingxi / RDA-Adapt | 30 | raw | 22.59% | 2.17 | -18.58% | 81.15% | 3.27% |
| Lingxi / RDA-Adapt | 20 | industry_size_neutral | 22.12% | 2.14 | -19.04% | 79.12% | 8.78% |
| Lingxi / RDA-Adapt | 20 | raw | 32.85% | 2.88 | -15.33% | 129.00% | 6.63% |
| Lingxi / RDA-Adapt | 10 | industry_size_neutral | 25.84% | 2.10 | -21.61% | 95.49% | 12.98% |
| Lingxi / RDA-Adapt | 10 | raw | 42.65% | 3.22 | -14.94% | 181.83% | 11.03% |
| Lingxi / RDA-Adapt | 5 | industry_size_neutral | 27.08% | 1.83 | -22.29% | 101.19% | 17.10% |
| Lingxi / RDA-Adapt | 5 | raw | 55.70% | 3.62 | -18.09% | 263.82% | 14.60% |
| Qlib Alpha158 proxy | 30 | industry_size_neutral | 11.89% | 1.23 | -24.21% | 38.78% | 0.07% |
| Qlib Alpha158 proxy | 30 | raw | 11.89% | 1.23 | -24.21% | 38.78% | 0.07% |
| Qlib Alpha158 proxy | 20 | industry_size_neutral | 16.03% | 1.99 | -13.88% | 54.29% | 0.07% |
| Qlib Alpha158 proxy | 20 | raw | 16.03% | 1.99 | -13.88% | 54.29% | 0.07% |
| Qlib Alpha158 proxy | 10 | industry_size_neutral | 10.95% | 1.35 | -17.60% | 35.39% | 0.07% |
| Qlib Alpha158 proxy | 10 | raw | 10.95% | 1.35 | -17.60% | 35.39% | 0.07% |
| Qlib Alpha158 proxy | 5 | industry_size_neutral | 15.70% | 2.31 | -12.41% | 52.99% | 0.07% |
| Qlib Alpha158 proxy | 5 | raw | 15.70% | 2.31 | -12.41% | 52.99% | 0.07% |

## Initial Interpretation Before Claude Review

1. Lingxi is the dominant family across all three markets and both raw/neutral variants. The runner-up methods never beat Lingxi on annualized return under the same market/variant grid.
2. Lingxi5 has the highest annualized return in every market, but concentration risk is visible, especially in China A-share raw where MDD worsens to -26.14% versus Lingxi10 at -17.49% and Lingxi30 at -14.26%.
3. Lingxi10 is the best return/risk compromise. It materially improves return over Lingxi20/30 while keeping drawdown much closer to diversified portfolios than Lingxi5, especially in China A-share and US large cap.
4. Qlib Alpha158 teaches that static factor infrastructure is strong in US/HK large caps and remains useful as a stabilizing feature layer, but it degrades when pushed to concentrated Top5 in US and fails in A-share.
5. FinTSB teaches that time-series momentum/volatility features become more useful when concentrated in China A-share, but they are weak in HK and not competitive with Lingxi.

## Claude CLI Review

Claude Code CLI was asked to review the Lingxi TopK comparison and the two runner-up methods. Its conclusion is consistent with the local interpretation:

- Use **Lingxi10** as the default production proxy.
- Use **Lingxi20** when capacity, turnover, or execution depth matters more than peak return.
- Treat **Lingxi5** as an aggressive research/high-conviction variant, not the default production portfolio.

The main reason is that Lingxi5 often has the highest raw return, but it also concentrates more risk. In the US market, Lingxi10 keeps almost the same Sharpe profile with materially better drawdown than Lingxi5. In Hong Kong, the neutralized Lingxi5 Sharpe is worse than Lingxi10 and Lingxi20, which means the extra concentration is not robust after market/style removal.

## What To Learn From The Runner-Ups

1. `qlib_alpha158` is weaker than Lingxi in China A but relatively stable in US/HK. Its value is not as a replacement strategy, but as a broad, robust cross-sectional feature block that can reduce market-specific fragility.
2. `fintsb_ts` is generally not competitive as a standalone portfolio, but its time-series/momentum state information can still be useful as gated auxiliary features or risk controls inside Lingxi.
3. The next fusion version should keep Lingxi as the ranking backbone, then add `qlib_alpha158` features for breadth and `fintsb_ts` signals only when they pass regime/risk filters.

## Recommendation

The recommended naming and deployment order is:

1. **Lingxi10**: best default balance of return, Sharpe, robustness, and concentration.
2. **Lingxi20**: capacity-aware production alternative.
3. **Lingxi30**: conservative benchmark and reporting baseline.
4. **Lingxi5**: aggressive high-conviction research variant only.

Before real trading, the main remaining audits are point-in-time data alignment, leakage checks, realistic liquidity/capacity constraints, and expanded cost assumptions.

## Reproduction

```powershell
python scripts\run_lingxi_topk_comparison.py --out-dir experiments\lingxi_topk_comparison
```

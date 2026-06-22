# Lingxi-Fusion Upgrade Validation

Date: 2026-06-22

This report validates whether the two runner-up algorithm families can improve the Lingxi series.

## Protocol

| Item | Setting |
|---|---|
| Backbone | Lingxi / RD-Agent-Quant / DoubleAdapt-family H5 proxy |
| Runner-up sources | Qlib Alpha158 proxy, FinTSB time-series proxy |
| Markets | China A-share CSI300, US large cap, HK large cap, crypto major |
| Test period | 2023-01-03 to 2025-12-31 |
| Crypto note | crypto universe has 20 assets, so Top30 is skipped |
| Portfolio | equal-weight, long-only, daily rebalance |
| Cost | single-side 10 bps |
| Variants | raw and industry/size neutralized |
| Output | `experiments/lingxi_fusion_validation/lingxi_fusion_validation_summary.csv` |

## Fusion Methods

| Method | Design | Purpose |
|---|---|---|
| `lingxi_fusion_lite` | daily z-scored Lingxi + 0.15 * Qlib Alpha158 score | Add stable broad cross-sectional factors |
| `lingxi_fusion_regime` | Lingxi + online FinTSB gate with weights 0/0.10/0.25 | Use time-series state only when lagged evidence supports it |
| `lingxi_fusion_full` | Fusion-Lite + online FinTSB gate | Test the complete runner-up feature transfer |

The FinTSB gate uses only lagged portfolio outcomes at least H=5 trading days behind the decision date.

## Main Conclusion

The upgrade validation does **not** justify replacing the default **Lingxi10** with a Fusion version.

The stronger conclusion is:

1. **Keep Lingxi10 as the default production proxy.**
2. **Do not add Qlib/FinTSB blindly to China A-share; both reduce performance there.**
3. **Keep Lingxi-Fusion-Regime as an experimental US Top5 sleeve.**
4. **Keep Lingxi-Fusion-Lite/Full as small neutral robustness experiments for crypto and HK, not as the default.**

## Lingxi10 Key Comparison

| Market | Variant | Lingxi10 ann/Sharpe/MDD | Best Fusion10 ann/Sharpe/MDD | Verdict |
|---|---|---:|---:|---|
| China A-share | raw | 113.78% / 6.04 / -17.49% | 105.77% / 5.67 / -18.82% | Fusion hurts |
| China A-share | neutral | 89.65% / 5.15 / -23.57% | 84.15% / 4.82 / -25.93% | Fusion hurts |
| US large cap | raw | 50.89% / 6.04 / -14.44% | 50.89% / 6.04 / -14.44% | No improvement |
| US large cap | neutral | 41.82% / 5.46 / -13.83% | 41.82% / 5.46 / -13.83% | No improvement |
| HK large cap | raw | 42.65% / 3.22 / -14.94% | 42.65% / 3.22 / -14.94% | No improvement |
| HK large cap | neutral | 25.84% / 2.10 / -21.61% | 25.93% / 2.11 / -21.14% | Tiny improvement |
| Crypto major | raw | 108.61% / 3.73 / -41.94% | 108.61% / 3.73 / -41.94% | No improvement |
| Crypto major | neutral | 72.57% / 2.56 / -45.06% | 75.45% / 2.67 / -44.01% | Small improvement |

## Positive Upgrade Cases

| Market | TopK | Variant | Original Lingxi | Best Fusion | Interpretation |
|---|---:|---|---:|---:|---|
| US large cap | 5 | raw | 61.33% / 6.09 / -18.39% | 65.92% / 6.44 / -19.00% | FinTSB gate improves return and Sharpe, with slightly worse drawdown |
| US large cap | 5 | neutral | 51.26% / 5.70 / -14.74% | 52.53% / 5.74 / -14.74% | Cleanest Fusion improvement |
| HK large cap | 20 | neutral | 22.12% / 2.14 / -19.04% | 22.21% / 2.15 / -18.78% | Small robustness gain |
| HK large cap | 10 | neutral | 25.84% / 2.10 / -21.61% | 25.93% / 2.11 / -21.14% | Small robustness gain |
| Crypto major | 10 | neutral | 72.57% / 2.56 / -45.06% | 75.45% / 2.67 / -44.01% | Qlib stabilizer helps neutral ranking |
| Crypto major | 5 | neutral | 121.12% / 3.21 / -40.67% | 121.73% / 3.22 / -39.60% | Full fusion slightly improves risk-adjusted result |

## Negative Evidence

China A-share is the decisive warning. Every Fusion variant underperforms the original Lingxi series across Top30/20/10/5 and raw/neutral variants.

For Lingxi10 China A-share:

| Method | Raw ann | Raw Sharpe | Raw MDD | Neutral ann | Neutral Sharpe | Neutral MDD |
|---|---:|---:|---:|---:|---:|---:|
| Lingxi10 | 113.78% | 6.04 | -17.49% | 89.65% | 5.15 | -23.57% |
| Fusion-Lite10 | 105.14% | 5.53 | -24.39% | 84.15% | 4.82 | -25.93% |
| Fusion-Regime10 | 105.77% | 5.67 | -18.82% | 83.02% | 4.86 | -24.21% |
| Fusion-Full10 | 102.92% | 5.56 | -24.39% | 82.14% | 4.75 | -25.93% |

This means the runner-up signals are not missing alpha for the strongest local A-share proxy. They are mostly lower-quality or redundant signals in that market.

## Gate Behavior

The FinTSB gate often chooses non-zero weights, so the test is not trivially inactive.

| Market | TopK | Regime non-zero gate days |
|---|---:|---:|
| China A-share | 10 | 220 / 727 |
| US large cap | 5 | 343 / 752 |
| HK large cap | 10 | 103 / 735 |
| Crypto major | 10 | 370 / 1094 |

The gate is active most often in US Top5 and crypto Top10, which matches the only areas where it produces meaningful improvements.

## Decision

Current default remains:

1. **Lingxi10**: default practical strategy.
2. **Lingxi20**: capacity-aware production alternative.
3. **Lingxi5**: aggressive research/high-conviction variant.

Upgrade candidates:

1. **Lingxi-Fusion-Regime-US5**: worth keeping as a US high-conviction experimental sleeve.
2. **Lingxi-Fusion-Lite-Crypto10-neutral**: worth keeping as a crypto neutral robustness experiment.
3. **Lingxi-Fusion-Regime-HK20-neutral**: worth tracking, but the improvement is too small to promote.

The runner-up algorithms are still valuable, but their value is conditional and market-specific. They should be used as gated auxiliary signals, not as permanent additions to every Lingxi portfolio.

## Reproduction

```powershell
python scripts\run_lingxi_fusion_validation.py --out-dir experiments\lingxi_fusion_validation
```


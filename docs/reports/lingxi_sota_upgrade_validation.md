# Lingxi10 / Lingxi5 SOTA Upgrade Validation

Date: 2026-06-23

This report completes the first engineering pass after the cross-domain time-series SOTA survey. The new papers were first converted into ARA packages, small benchmark datasets were registered/downloaded, and lightweight SOTA-inspired proxies were tested against Lingxi10/Lingxi5.

## ARA Engineering

| Item | Result |
|---|---:|
| New cross-domain SOTA papers | 14 |
| New ARA packages | 14 |
| ARA Level 1 validation | 14 / 14 PASS |
| Summary file | `ara_artifacts/cross_domain_sota_ara_summary.csv` |
| Candidate metadata | `papers/metadata/lingxi_cross_domain_ts_sota_candidates.csv` |

The new ARA packages are methodology-transfer artifacts, not official reproductions. Each package explicitly marks official code import and local proxy validation status separately.

## Dataset Handling

The papers commonly reference long-horizon time-series datasets. To avoid uncontrolled large-data vendoring, only the small ETT benchmark files were downloaded in this pass.

| Dataset | Rows | Columns | Local file |
|---|---:|---:|---|
| ETTh1 | 17,420 | 8 | `data/external/time_series_sota/ett/ETTh1.csv` |
| ETTh2 | 17,420 | 8 | `data/external/time_series_sota/ett/ETTh2.csv` |
| ETTm1 | 69,680 | 8 | `data/external/time_series_sota/ett/ETTm1.csv` |
| ETTm2 | 69,680 | 8 | `data/external/time_series_sota/ett/ETTm2.csv` |

Profile and checksums are in `data/external/time_series_sota/dataset_profile.csv`. Larger datasets such as Weather, Electricity, Traffic, M4, Monash, UCR/UEA, and PEMS are registered in `papers/metadata/lingxi_cross_domain_ts_datasets.csv` but kept as documented-only.

## ETT Sanity Benchmark

The downloaded ETT files were also used for a small non-financial forecasting sanity benchmark. This does not reproduce any official paper result; it checks that the local generic time-series pipeline can distinguish a simple linear decomposition proxy from a naive last-value baseline.

Settings:

- Target: `OT`
- Lookback: 96
- Horizon: 96
- Split: chronological 60% train, 20% validation gap/holdout, 20% test
- Output: `experiments/cross_domain_ts_datasets/ett_linear_guard_summary.csv`

| Dataset | Naive MAE/RMSE/sMAPE | DLinear-style MAE/RMSE/sMAPE | Result |
|---|---:|---:|---|
| ETTh1 | 2.8679 / 3.6905 / 0.4306 | 2.4769 / 3.1476 / 0.3680 | LinearGuard better |
| ETTh2 | 6.1255 / 7.9794 / 0.2795 | 5.4684 / 6.8534 / 0.2384 | LinearGuard better |
| ETTm1 | 1.7199 / 2.2478 / 0.3043 | 1.6630 / 2.2243 / 0.2699 | LinearGuard better |
| ETTm2 | 3.5162 / 4.7641 / 0.1670 | 3.4775 / 4.6398 / 0.1573 | LinearGuard better |

MAPE is present in the CSV but should not be used for ETTh1/ETTm1 because near-zero `OT` values make it unstable.

## Tested Proxies

| Proxy | Source methods | Local interpretation |
|---|---|---|
| `lingxi_linear_guard` | DLinear / LTSF-Linear | Decomposition-linear sanity baseline |
| `lingxi_pitnorm` | Non-stationary Transformer / rolling stationarization | Point-in-time rolling normalization of Lingxi scores |
| `lingxi_mscale` | TimeMixer / N-HiTS / FEDformer | Multi-scale trend, reversal, volatility, and range features |
| `lingxi_patch` | PatchTST / TTM | Patch-summary OHLCV feature proxy |
| `lingxi_varattn` | iTransformer | Lightweight cross-sectional feature-attention proxy |

Protocol:

- Markets: China A-share CSI300, US large cap, HK large cap, crypto major
- Label: H5
- Portfolio: Top10 and Top5, equal-weight, long-only, daily rebalance
- Cost: single-side 10 bps
- Variants: raw and industry/size neutral where applicable
- Output: `experiments/lingxi_sota_upgrade_validation/lingxi_sota_upgrade_validation_summary.csv`

## Main Result

No SOTA-inspired proxy should replace Lingxi10 or Lingxi5 as the main strategy yet.

The useful result is narrower:

1. **Lingxi-PITNorm is a real risk-control upgrade candidate.**
2. **Lingxi-PITNorm improves Sharpe/drawdown in several stock-market raw or neutral settings, but usually sacrifices annualized return.**
3. **LinearGuard, MScale, Patch, and VarAttn proxies do not beat Lingxi10/5.**
4. **The simple VarAttn proxy is not enough to validate or reject iTransformer itself; it only rejects this cheap approximation.**

## Key Comparisons

### China A-share

| TopK | Variant | Lingxi ann/Sharpe/MDD | Best SOTA proxy ann/Sharpe/MDD | Interpretation |
|---:|---|---:|---:|---|
| 10 | raw | 113.78% / 6.04 / -17.49% | PITNorm 96.89% / 6.78 / -12.20% | lower return, much better risk |
| 10 | neutral | 89.65% / 5.15 / -23.57% | Lingxi remains best | keep original |
| 5 | raw | 156.66% / 6.62 / -26.14% | PITNorm 119.28% / 7.29 / -12.35% | strong risk-control variant |
| 5 | neutral | 116.66% / 5.50 / -25.46% | Lingxi remains best | keep original |

### US Large Cap

| TopK | Variant | Lingxi ann/Sharpe/MDD | Best SOTA proxy ann/Sharpe/MDD | Interpretation |
|---:|---|---:|---:|---|
| 10 | raw | 50.89% / 6.04 / -14.44% | PITNorm 46.23% / 6.14 / -11.50% | small Sharpe/drawdown gain |
| 10 | neutral | 41.82% / 5.46 / -13.83% | PITNorm 40.72% / 5.71 / -14.04% | Sharpe gain but no drawdown gain |
| 5 | raw | 61.33% / 6.09 / -18.39% | Lingxi remains best | keep original |
| 5 | neutral | 51.26% / 5.70 / -14.74% | Lingxi remains best | keep original |

### HK Large Cap

| TopK | Variant | Lingxi ann/Sharpe/MDD | Best SOTA proxy ann/Sharpe/MDD | Interpretation |
|---:|---|---:|---:|---|
| 10 | raw | 42.65% / 3.22 / -14.94% | PITNorm 46.21% / 3.49 / -15.63% | return/Sharpe gain, slight drawdown cost |
| 10 | neutral | 25.84% / 2.10 / -21.61% | PITNorm 31.42% / 2.60 / -18.88% | clean improvement |
| 5 | raw | 55.70% / 3.62 / -18.09% | PITNorm 51.17% / 3.68 / -14.38% | risk-control improvement |
| 5 | neutral | 27.08% / 1.83 / -22.29% | PITNorm 36.56% / 2.74 / -21.17% | clean improvement |

### Crypto Major

| TopK | Variant | Lingxi ann/Sharpe/MDD | Best SOTA proxy ann/Sharpe/MDD | Interpretation |
|---:|---|---:|---:|---|
| 10 | raw | 108.61% / 3.73 / -41.94% | Lingxi remains best | keep original |
| 10 | neutral | 72.57% / 2.56 / -45.06% | Lingxi remains best | keep original |
| 5 | raw | 192.32% / 4.77 / -43.75% | Lingxi remains best | keep original |
| 5 | neutral | 121.12% / 3.21 / -40.67% | Lingxi remains best | keep original |

## Decision

Current mainline remains:

1. **Lingxi10**: default strategy.
2. **Lingxi5**: high-conviction/aggressive strategy.

New candidate:

1. **Lingxi-PITNorm10**: risk-controlled version of Lingxi10.
2. **Lingxi-PITNorm5**: high-conviction strategy with substantially lower A-share raw drawdown, but materially lower return.
3. **Lingxi-PITNorm-HK**: strongest market-specific upgrade signal in this run.

Rejected as first-pass replacements:

- `lingxi_linear_guard`
- `lingxi_mscale`
- `lingxi_patch`
- `lingxi_varattn`

These rejected proxies are still useful as negative evidence. They show that generic SOTA-inspired feature extraction is not enough; the only robust gain came from a non-stationarity treatment applied directly to the already-strong Lingxi score.

## Next Engineering Step

The next upgrade should not expand to more raw feature proxies. It should focus on:

1. **PITNorm gating**: switch between original Lingxi and PITNorm only when lagged drawdown/volatility risk justifies it.
2. **Closer iTransformer implementation**: build a real cross-sectional variate-token learner instead of the cheap feature-attention approximation.
3. **Official PatchTST/iTransformer lightweight reproduction**: only after PITNorm gating is evaluated.
4. **ETT benchmark sanity run**: use downloaded ETT files to verify the local proxy code on generic forecasting before claiming method fidelity.

## Reproduction

```powershell
python scripts\build_cross_domain_sota_ara.py
python scripts\download_cross_domain_ts_datasets.py --retries 5
python scripts\run_ett_linear_guard_benchmark.py
python scripts\run_lingxi_sota_upgrade_validation.py --out-dir experiments\lingxi_sota_upgrade_validation
```

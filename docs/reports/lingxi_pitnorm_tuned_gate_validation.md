# Lingxi-PITNorm Tuned Gate Validation

Date: 2026-06-23

This experiment follows the first dynamic PITNorm gate by adding two refinements:

1. **ReturnFloor-Gate**: penalizes candidate gate weights whose lagged mean return falls too far below the original Lingxi baseline.
2. **ReturnFloor-HKBias-Gate**: adds a small PITNorm persistence bias for HK to test whether the previous HK under-selection can be fixed online.

## Protocol

| Item | Setting |
|---|---|
| Base strategies | Lingxi10, Lingxi5 |
| Candidate adapter | Lingxi-PITNorm |
| Gate weights | 0.0, 0.5, 1.0 |
| Variant handling | raw and neutral gates are selected separately |
| Return floor | candidate lagged mean should stay near original Lingxi lagged mean |
| HK bias | +0.00025 * PITNorm weight for HK only |
| Markets | China A-share CSI300, US large cap, HK large cap, crypto major |
| Output | `experiments/lingxi_pitnorm_tuned_gate_validation/lingxi_pitnorm_tuned_gate_validation_summary.csv` |

## Main Conclusion

ReturnFloor helps, but it does not create one universal best gate.

The practical strategy family is now clearer:

1. **Default remains Lingxi10 / Lingxi5.**
2. **Use ReturnFloor-Gate for US Top5 raw/neutral and crypto raw.**
3. **Use static PITNorm for HK.** HK bias did not outperform static PITNorm.
4. **Use ReturnFloor-Gate as an A-share Top5 neutral risk-adjusted sleeve, not as the headline A-share Top5.**
5. **Do not use tuned gates for A-share neutral Top10 or crypto neutral.**

## Best By Scenario

| Market | TopK | Variant | Best method | Ann. return | Sharpe | MDD |
|---|---:|---|---|---:|---:|---:|
| China A-share | 10 | raw | PITNorm | 96.89% | 6.78 | -12.20% |
| China A-share | 10 | neutral | Lingxi | 89.65% | 5.15 | -23.57% |
| China A-share | 5 | raw | PITNorm | 119.28% | 7.29 | -12.35% |
| China A-share | 5 | neutral | ReturnFloor-Gate | 103.63% | 6.00 | -16.41% |
| US large cap | 10 | raw | PITNorm | 46.23% | 6.14 | -11.50% |
| US large cap | 10 | neutral | PITNorm | 40.72% | 5.71 | -14.04% |
| US large cap | 5 | raw | ReturnFloor-Gate | 61.71% | 6.53 | -10.23% |
| US large cap | 5 | neutral | ReturnFloor-Gate | 51.09% | 5.95 | -13.93% |
| HK large cap | 10 | raw | PITNorm | 46.21% | 3.49 | -15.63% |
| HK large cap | 10 | neutral | PITNorm | 31.42% | 2.60 | -18.88% |
| HK large cap | 5 | raw | PITNorm | 51.17% | 3.68 | -14.38% |
| HK large cap | 5 | neutral | PITNorm | 36.56% | 2.74 | -21.17% |
| Crypto major | 10 | raw | ReturnFloor-Gate | 111.34% | 3.82 | -42.66% |
| Crypto major | 10 | neutral | Lingxi | 72.57% | 2.56 | -45.06% |
| Crypto major | 5 | raw | ReturnFloor-Gate | 195.10% | 4.97 | -38.82% |
| Crypto major | 5 | neutral | Lingxi | 121.12% | 3.21 | -40.67% |

## Important Improvements

### US Top5

| Variant | Lingxi | Previous Gate | ReturnFloor-Gate | Decision |
|---|---:|---:|---:|---|
| raw | 61.33% / 6.09 / -18.39% | 60.78% / 6.43 / -10.46% | 61.71% / 6.53 / -10.23% | Promote ReturnFloor-Gate |
| neutral | 51.26% / 5.70 / -14.74% | 49.34% / 5.78 / -12.36% | 51.09% / 5.95 / -13.93% | Promote ReturnFloor-Gate |

### Crypto Raw

| TopK | Lingxi | Previous Gate | ReturnFloor-Gate | Decision |
|---:|---:|---:|---:|---|
| 10 | 108.61% / 3.73 / -41.94% | 111.93% / 3.85 / -42.33% | 111.34% / 3.82 / -42.66% | Previous and ReturnFloor both useful |
| 5 | 192.32% / 4.77 / -43.75% | 195.78% / 4.98 / -38.92% | 195.10% / 4.97 / -38.82% | Promote ReturnFloor-Gate |

### A-share Top5 Neutral

| Method | Ann. return | Sharpe | MDD |
|---|---:|---:|---:|
| Lingxi | 116.66% | 5.50 | -25.46% |
| PITNorm | 65.47% | 4.63 | -18.30% |
| ReturnFloor-Gate | 103.63% | 6.00 | -16.41% |

This is a real risk-adjusted improvement, but it gives up about 13 percentage points of annualized return versus original Lingxi. It should be a risk-controlled sleeve, not the headline A-share Top5.

## Failed Tuning

HK bias did not fix the HK online gate. Static PITNorm remains better in all HK Top10/Top5 raw/neutral cases.

Interpretation: HK does not need a more aggressive online PITNorm selector; it needs a simple static rule: use PITNorm for HK risk-controlled variants.

## Updated Strategy Menu

| Use case | Recommended method |
|---|---|
| Headline A-share Top10 | Lingxi10 |
| A-share Top10 raw risk-adjusted sleeve | PITNorm or previous gate |
| A-share Top5 headline | Lingxi5 |
| A-share Top5 neutral risk-controlled sleeve | ReturnFloor-Gate |
| US Top10 | PITNorm if Sharpe/drawdown matters, Lingxi if return matters |
| US Top5 | ReturnFloor-Gate |
| HK Top10/Top5 | Static PITNorm |
| Crypto raw Top10/Top5 | ReturnFloor-Gate |
| Crypto neutral Top10/Top5 | Lingxi |

## Next Experiment

The next experiment should stop adding generic gate complexity and instead build a **strategy selector table**:

1. Encode the recommended method per market/topk/variant.
2. Produce one final "Lingxi Adaptive Suite" report.
3. Optionally test portfolio-level blending across sleeves rather than score-level gating.

## Reproduction

```powershell
python scripts\run_lingxi_pitnorm_tuned_gate_validation.py --out-dir experiments\lingxi_pitnorm_tuned_gate_validation
```

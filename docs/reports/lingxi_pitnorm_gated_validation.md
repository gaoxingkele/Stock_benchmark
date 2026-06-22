# Lingxi-PITNorm Dynamic Gate Validation

Date: 2026-06-23

This report validates the next step after the SOTA-inspired upgrade run: dynamic gating between the original Lingxi score and Lingxi-PITNorm.

## Protocol

| Item | Setting |
|---|---|
| Base strategies | Lingxi10, Lingxi5 |
| Candidate adapter | Lingxi-PITNorm |
| Gate weights | 0.0, 0.5, 1.0 |
| Gate information | Lagged portfolio outcomes only, at least H=5 trading days behind the decision date |
| Gate objective | Mean return minus volatility, drawdown, and turnover penalties |
| Markets | China A-share CSI300, US large cap, HK large cap, crypto major |
| Label | H5 |
| Cost | single-side 10 bps |
| Output | `experiments/lingxi_pitnorm_gated_validation/lingxi_pitnorm_gated_validation_summary.csv` |

## Main Conclusion

Dynamic gating is useful, but not as a universal replacement.

Recommended production/research split:

1. **Keep original Lingxi10 as the default headline strategy.**
2. **Use Lingxi-PITNorm-Gate for A-share Top10 raw and crypto raw sleeves.**
3. **Use Lingxi-PITNorm-Gate for US Top5, where it improves Sharpe and drawdown while keeping most return.**
4. **Use static Lingxi-PITNorm for HK risk-controlled variants; the online gate under-selects PITNorm there.**
5. **Keep original Lingxi for A-share neutral and crypto neutral variants.**

## Top10 Results

| Market | Variant | Best method | Ann. return | Sharpe | MDD | Interpretation |
|---|---|---|---:|---:|---:|---|
| China A-share | raw | PITNorm-Gate | 111.41% | 6.85 | -14.83% | Best risk-adjusted balance; near Lingxi return with lower drawdown |
| China A-share | neutral | Lingxi | 89.65% | 5.15 | -23.57% | PITNorm cuts too much return |
| US large cap | raw | PITNorm | 46.23% | 6.14 | -11.50% | Static PITNorm has best Sharpe/drawdown |
| US large cap | neutral | PITNorm | 40.72% | 5.71 | -14.04% | Static PITNorm best Sharpe, but Lingxi has higher return |
| HK large cap | raw | PITNorm | 46.21% | 3.49 | -15.63% | Static PITNorm beats gate |
| HK large cap | neutral | PITNorm | 31.42% | 2.60 | -18.88% | Clean static PITNorm improvement |
| Crypto major | raw | PITNorm-Gate | 111.93% | 3.85 | -42.33% | Better return and Sharpe than Lingxi |
| Crypto major | neutral | Lingxi | 72.57% | 2.56 | -45.06% | Original remains best |

## Top5 Results

| Market | Variant | Best method | Ann. return | Sharpe | MDD | Interpretation |
|---|---|---|---:|---:|---:|---|
| China A-share | raw | PITNorm | 119.28% | 7.29 | -12.35% | Strongest risk-control variant, but far below Lingxi return |
| China A-share | neutral | Lingxi | 116.66% | 5.50 | -25.46% | Original remains best |
| US large cap | raw | PITNorm-Gate | 60.78% | 6.43 | -10.46% | Best Top5 upgrade case |
| US large cap | neutral | PITNorm-Gate | 49.34% | 5.78 | -12.36% | Best risk-adjusted neutral version |
| HK large cap | raw | PITNorm | 51.17% | 3.68 | -14.38% | Static PITNorm better than gate |
| HK large cap | neutral | PITNorm | 36.56% | 2.74 | -21.17% | Static PITNorm best |
| Crypto major | raw | PITNorm-Gate | 195.78% | 4.98 | -38.92% | Best return, Sharpe, and drawdown |
| Crypto major | neutral | Lingxi | 121.12% | 3.21 | -40.67% | Original remains best |

## Gate Activity

| Market | TopK | Original days | Half-PITNorm days | Full-PITNorm days |
|---|---:|---:|---:|---:|
| China A-share | 10 | 153 | 152 | 422 |
| China A-share | 5 | 177 | 155 | 395 |
| US large cap | 10 | 257 | 151 | 344 |
| US large cap | 5 | 221 | 248 | 283 |
| HK large cap | 10 | 261 | 135 | 339 |
| HK large cap | 5 | 301 | 40 | 394 |
| Crypto major | 10 | 553 | 281 | 260 |
| Crypto major | 5 | 575 | 265 | 254 |

The gate is active enough to be meaningful. Its weakness is not inactivity; it is that the current rolling objective sometimes fails to select the better static PITNorm policy in HK.

## Decision

Do not replace Lingxi10/5 with one universal gated model.

Adopt this strategy family:

| Use case | Recommended method |
|---|---|
| Default headline Top10 | Lingxi10 |
| Default high-conviction Top5 | Lingxi5 |
| A-share Top10 raw risk-adjusted sleeve | Lingxi-PITNorm-Gate10 |
| A-share Top5 raw low-drawdown sleeve | Lingxi-PITNorm5 |
| US Top5 raw/neutral | Lingxi-PITNorm-Gate5 |
| HK Top10/Top5 neutral | Lingxi-PITNorm static |
| Crypto Top10/Top5 raw | Lingxi-PITNorm-Gate |
| Crypto neutral | Lingxi original |

## Next Step

The next engineering step should tune the gate objective by market and variant:

1. Add a **return floor** so the gate does not over-select PITNorm when it protects drawdown but gives up too much alpha.
2. Add a **HK-specific persistence bias** toward static PITNorm after it has demonstrated a clean neutral advantage.
3. Add a **neutral-aware gate**, because raw and neutral winners differ materially.
4. Re-run with Top10/Top5 only, then promote a small set of named variants instead of a single universal strategy.

## Reproduction

```powershell
python scripts\run_lingxi_pitnorm_gated_validation.py --out-dir experiments\lingxi_pitnorm_gated_validation
```

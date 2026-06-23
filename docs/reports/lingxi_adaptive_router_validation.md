# Lingxi Adaptive Router Validation

Date: 2026-06-23

## Objective

Validate whether a dynamic strategy router can switch between:

- Lingxi
- Lingxi-PITNorm
- Lingxi-PITNorm ReturnFloor-Gate

The router uses only lagged daily strategy outcomes and market context. It is tested against fixed strategies, a static equal ensemble, and a non-tradable oracle upper bound.

## Protocol

| Item | Setting |
|---|---|
| Markets | China A-share CSI300, US large cap, HK large cap, crypto major |
| TopK | 10, 5 |
| Variants | raw, industry/size neutral |
| Source strategies | `experiments/lingxi_pitnorm_tuned_gate_validation/` |
| 2026 YTD source | `experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/` |
| Router horizon lag | 5 trading days |
| Router context | lagged benchmark return, volatility, drawdown, strategy return, Sharpe, drawdown, turnover, industry concentration, size exposure |
| Router methods | rolling selector, Hedge, contextual ridge |
| Upper bound | same-day oracle, not tradable |

Reproduction:

```powershell
python scripts\run_lingxi_adaptive_router_validation.py --out-dir experiments\lingxi_adaptive_router_validation
python scripts\run_lingxi_pitnorm_tuned_gate_validation.py --test-end 2026-06-18 --out-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd
python scripts\run_lingxi_adaptive_router_validation.py --source-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd --out-dir experiments\lingxi_adaptive_router_validation_2026_ytd
```

## Main Conclusion

The first adaptive router is useful as a research direction, but it is **not strong enough to replace the fixed strategy menu**.

Evidence:

- In the 2023-2025 sample, the best router beats the best fixed/static baseline by Sharpe in only 3 of 16 scenarios.
- In the 2023-2026 YTD sample, this drops to 2 of 16 scenarios.
- The oracle upper bound is much higher than all tradable routers, so route timing has theoretical room, but the current lagged feature set does not capture enough of that room.
- Contextual ridge is the most promising router, but its advantage is concentrated in a few scenarios.
- Hedge is stable but behaves more like a slow dynamic ensemble than a decisive router.
- Rolling selector is interpretable, but often chases recent winners too late.

The practical decision is: keep the current fixed/scene-specific Lingxi menu as the production proxy, and treat adaptive routing as a second-layer research module.

## 2023-2025 Best Router vs Best Fixed/Static Baseline

| Scenario | Best fixed/static | Ann. / Sharpe / MDD | Best router | Ann. / Sharpe / MDD | Router wins? |
|---|---|---:|---|---:|---|
| A-share Top10 raw | Static ensemble | 107.51% / 6.97 / -13.35% | Contextual ridge | 118.38% / 7.12 / -11.44% | Yes |
| A-share Top10 neutral | Lingxi | 89.65% / 5.15 / -23.57% | Contextual ridge | 78.88% / 5.23 / -16.02% | Yes, risk-adjusted |
| A-share Top5 raw | Static ensemble | 137.79% / 7.64 / -12.16% | Contextual ridge | 147.82% / 7.51 / -17.85% | No |
| A-share Top5 neutral | ReturnFloor-Gate | 103.63% / 6.00 / -16.41% | Rolling selector | 98.41% / 5.67 / -25.19% | No |
| US Top10 raw | Static ensemble | 47.74% / 6.15 / -13.84% | Hedge | 47.15% / 5.85 / -14.15% | No |
| US Top10 neutral | PITNorm | 40.72% / 5.71 / -14.04% | Rolling selector | 40.27% / 5.49 / -14.04% | No |
| US Top5 raw | Static ensemble | 58.05% / 6.68 / -11.54% | Hedge | 57.28% / 6.01 / -13.91% | No |
| US Top5 neutral | Static ensemble | 48.04% / 6.03 / -13.65% | Rolling selector | 50.00% / 5.80 / -13.96% | No |
| HK Top10 raw | PITNorm | 46.21% / 3.49 / -15.63% | Contextual ridge | 43.40% / 3.39 / -15.49% | No |
| HK Top10 neutral | PITNorm | 31.42% / 2.60 / -18.88% | Rolling selector | 32.07% / 2.58 / -21.10% | No |
| HK Top5 raw | PITNorm | 51.17% / 3.68 / -14.38% | Contextual ridge | 54.57% / 3.68 / -17.70% | No |
| HK Top5 neutral | PITNorm | 36.56% / 2.74 / -21.17% | Rolling selector | 33.60% / 2.44 / -19.70% | No |
| Crypto Top10 raw | ReturnFloor-Gate | 111.34% / 3.82 / -42.66% | Rolling selector | 110.65% / 3.79 / -43.03% | No |
| Crypto Top10 neutral | Lingxi | 72.57% / 2.56 / -45.06% | Contextual ridge | 69.01% / 2.47 / -45.34% | No |
| Crypto Top5 raw | ReturnFloor-Gate | 195.10% / 4.97 / -38.82% | Hedge | 184.46% / 4.74 / -38.10% | No |
| Crypto Top5 neutral | Lingxi | 121.12% / 3.21 / -40.67% | Contextual ridge | 124.74% / 3.34 / -38.62% | Yes |

## 2026 YTD Stability Check

Adding 2026 YTD weakens the dynamic-router claim:

- Router Sharpe wins fall from 3/16 to 2/16.
- A-share Top10 raw no longer favors contextual ridge over static ensemble by Sharpe.
- Crypto Top10 raw becomes a small rolling-selector win.
- Crypto Top5 neutral remains a contextual-ridge win.
- HK remains a PITNorm market.
- US remains better served by static/fixed baselines.

Important 2026 YTD cases:

| Scenario | Best fixed/static | Ann. / Sharpe / MDD | Best router | Ann. / Sharpe / MDD | Router wins? |
|---|---|---:|---|---:|---|
| A-share Top10 raw | Static ensemble | 116.40% / 7.65 / -13.35% | Rolling selector | 120.08% / 7.45 / -13.99% | No |
| A-share Top10 neutral | Lingxi | 100.75% / 5.86 / -23.57% | Hedge | 88.62% / 5.74 / -21.92% | No |
| Crypto Top10 raw | ReturnFloor-Gate | 72.62% / 2.59 / -60.15% | Rolling selector | 72.95% / 2.59 / -59.31% | Yes, small |
| Crypto Top5 neutral | Lingxi | 79.08% / 2.21 / -62.04% | Contextual ridge | 79.99% / 2.25 / -63.49% | Yes, small |

## Router Diagnostics

Average router behavior:

| Sample | Router | Avg. Sharpe | Avg. switch rate |
|---|---|---:|---:|
| 2023-2025 | rolling selector | 4.46 | 2.58% |
| 2023-2025 | Hedge | 4.45 | 0.00% |
| 2023-2025 | contextual ridge | 4.58 | 7.84% |
| 2023-2026 YTD | rolling selector | 4.16 | 2.66% |
| 2023-2026 YTD | Hedge | 4.28 | 0.00% |
| 2023-2026 YTD | contextual ridge | 4.26 | 7.93% |

Interpretation:

- Contextual ridge is the best research candidate, but its switching rate is materially higher.
- Hedge has low operational friction, but it is too slow to exploit regime changes.
- Rolling selector is easy to explain, but the lagged winner often stops winning.

## LLM / Multi-Agent Debate Position

The current evidence does not support letting LLMs directly choose the trading route.

LLM usage should be limited to a second-stage macro context adapter:

1. Convert external text into structured tags such as `risk_on`, `policy_supportive`, `liquidity_tightening`, or `sector_rotation_high`.
2. Feed those tags into the same router as additional lagged context.
3. Compare against the no-LLM router in the same out-of-sample protocol.
4. Use multi-LLM debate for explanation and audit, not direct execution.

The reason is reproducibility: direct LLM decisions are unstable, hard to backtest cleanly, and hard to audit for hidden future information.

## Updated Strategy Decision

Use this production-facing menu:

| Use case | Recommended method |
|---|---|
| A-share Top10 raw | Static ensemble or contextual ridge research sleeve |
| A-share Top10 neutral | Lingxi headline; contextual ridge only as risk-adjusted research sleeve |
| A-share Top5 raw | Lingxi for return, static ensemble for Sharpe/drawdown |
| A-share Top5 neutral | ReturnFloor-Gate |
| US Top10/Top5 | Static/fixed baselines, not router |
| HK Top10/Top5 | PITNorm |
| Crypto Top10 raw | ReturnFloor-Gate; rolling selector is only a small 2026 YTD improvement |
| Crypto Top5 raw | ReturnFloor-Gate |
| Crypto Top5 neutral | Contextual ridge research sleeve; Lingxi remains simpler baseline |

## Next Research Step

Do not add a full RL agent yet. The data does not justify the complexity.

Next experiment should test whether richer context improves route timing:

1. Add explicit market-regime features from the underlying panel, not only strategy daily returns.
2. Add stress-state features: volatility percentile, drawdown percentile, market breadth, and cross-sectional dispersion.
3. Add LLM macro tags only after the structured regime router is stable.
4. Compare with the current contextual ridge router as the benchmark.

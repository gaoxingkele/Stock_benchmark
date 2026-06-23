# Lingxi Market-Regime Router Validation

Date: 2026-06-23

## Objective

Test whether adding structured market-regime context improves the Lingxi adaptive router.

The previous adaptive router used mainly lagged strategy returns and benchmark returns. This experiment adds features from the underlying market panel:

- market equal-weight return
- 20/60 day momentum
- 20/60 day realized volatility
- 60 day drawdown
- daily and 20 day breadth
- cross-sectional dispersion
- 20 day return tail spread
- amount/liquidity change
- size concentration
- top-20% size share

The router still uses only lagged information at least 5 trading days behind the decision date.

## Protocol

| Item | Setting |
|---|---|
| Sample | 2023-01-03 to 2026 YTD |
| Source strategies | `experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/` |
| Markets | China A-share, US large cap, HK large cap, crypto major |
| TopK | 10, 5 |
| Variants | raw, industry/size neutral |
| New router | `market_regime_ridge_router` |
| Comparison | fixed sleeves, static ensemble, contextual ridge, oracle upper bound |
| Output | `experiments/lingxi_regime_router_validation_2026_ytd/` |

Reproduction:

```powershell
python scripts\run_lingxi_regime_router_validation.py --out-dir experiments\lingxi_regime_router_validation_2026_ytd
```

## Main Conclusion

Market-regime features provide **some real incremental information**, but still do not justify replacing the fixed/scene-specific strategy menu.

Evidence:

- Regime ridge beats the previous contextual ridge by Sharpe in 9 of 16 scenarios.
- Regime ridge beats the best fixed/static baseline by Sharpe in only 2 of 16 scenarios.
- The two strongest cases are A-share Top5 neutral and crypto Top5 raw.
- The feature expansion hurts important cases such as A-share Top10 raw, A-share Top5 raw, US neutral, and crypto Top5 neutral.

This is a useful research result: market context matters, but a larger feature set also increases estimation noise. The current regime router should be treated as a selective research sleeve, not a production router.

## Scenario Results

| Scenario | Best fixed/static | Ann. / Sharpe / MDD | Contextual ridge | Regime ridge | Regime vs fixed | Regime vs contextual |
|---|---|---:|---:|---:|---|---|
| A-share Top10 raw | Static ensemble | 116.40% / 7.65 / -13.35% | 125.31% / 7.59 / -11.44% | 119.63% / 6.91 / -13.38% | No | No |
| A-share Top10 neutral | Lingxi | 100.75% / 5.86 / -23.57% | 83.97% / 5.62 / -16.02% | 85.51% / 5.71 / -15.30% | No | Yes |
| A-share Top5 raw | Static ensemble | 137.79% / 7.78 / -12.16% | 147.68% / 7.47 / -19.89% | 129.17% / 6.09 / -15.08% | No | No |
| A-share Top5 neutral | Lingxi | 130.65% / 6.17 / -25.46% | 109.64% / 6.12 / -17.64% | 113.95% / 6.36 / -15.36% | Yes | Yes |
| US Top10 raw | PITNorm | 49.52% / 6.11 / -11.60% | 48.03% / 5.61 / -14.41% | 49.81% / 5.79 / -12.85% | No | Yes |
| US Top10 neutral | Lingxi | 42.54% / 5.38 / -14.26% | 38.58% / 4.93 / -16.28% | 37.92% / 4.92 / -18.56% | No | No |
| US Top5 raw | Static ensemble | 64.11% / 6.76 / -12.21% | 57.43% / 5.63 / -15.02% | 59.04% / 5.78 / -15.46% | No | Yes |
| US Top5 neutral | Static ensemble | 48.69% / 5.69 / -16.36% | 48.95% / 5.26 / -17.42% | 47.75% / 5.13 / -19.02% | No | No |
| HK Top10 raw | PITNorm | 41.60% / 3.30 / -15.63% | 38.87% / 3.18 / -15.49% | 37.87% / 3.12 / -14.94% | No | No |
| HK Top10 neutral | PITNorm | 28.01% / 2.43 / -18.88% | 24.90% / 2.20 / -19.26% | 25.23% / 2.21 / -19.69% | No | Yes |
| HK Top5 raw | PITNorm | 45.98% / 3.47 / -14.38% | 47.86% / 3.39 / -18.09% | 46.93% / 3.39 / -17.70% | No | Yes |
| HK Top5 neutral | PITNorm | 33.28% / 2.58 / -21.17% | 30.83% / 2.30 / -17.83% | 32.27% / 2.43 / -18.58% | No | Yes |
| Crypto Top10 raw | ReturnFloor-Gate | 72.62% / 2.59 / -60.15% | 69.09% / 2.48 / -59.10% | 70.55% / 2.53 / -59.86% | No | Yes |
| Crypto Top10 neutral | Lingxi | 47.70% / 1.75 / -59.87% | 46.67% / 1.72 / -60.23% | 44.30% / 1.64 / -58.43% | No | No |
| Crypto Top5 raw | ReturnFloor-Gate | 128.98% / 3.45 / -58.91% | 123.47% / 3.23 / -61.65% | 135.15% / 3.53 / -58.77% | Yes | Yes |
| Crypto Top5 neutral | Lingxi | 79.08% / 2.21 / -62.04% | 79.50% / 2.23 / -63.57% | 62.08% / 1.80 / -62.25% | No | No |

## Interpretation

The regime features improve the router when the market state aligns with a clear sleeve preference:

- A-share Top5 neutral: regime features help reduce drawdown while improving Sharpe.
- Crypto Top5 raw: regime features help time ReturnFloor/PITNorm/Lingxi switches in a high-volatility market.
- HK neutral cases: regime features improve over contextual ridge, but still do not beat PITNorm.

They hurt when the added context creates estimation noise:

- A-share Top10 raw and Top5 raw already have very strong fixed/static baselines.
- US large cap has stable enough sleeve behavior that added regime context does not help.
- Crypto Top5 neutral is better handled by simpler Lingxi/contextual behavior.

## LLM Implication

This result is important for the LLM idea.

If clean numerical regime features only beat fixed/static baselines in 2 of 16 scenarios, then free-form LLM macro debate should not be allowed to directly control routing. The next LLM experiment must be stricter:

1. Generate dated structured macro tags only.
2. Freeze those tags before backtest evaluation.
3. Add them to this regime router as extra features.
4. Require improvement over both contextual ridge and fixed/static baselines.

The LLM module should be an adapter, not the decision maker.

## Updated Decision

Promote only two regime-router sleeves to the research menu:

| Sleeve | Decision |
|---|---|
| A-share Top5 neutral market-regime ridge | Keep as research candidate |
| Crypto Top5 raw market-regime ridge | Keep as research candidate |
| All US regime routers | Reject for now |
| HK regime routers | Reject as production; PITNorm remains better |
| A-share raw regime routers | Reject; static ensemble/contextual or Lingxi is better |
| Crypto neutral regime routers | Reject |

## Next Step

The next meaningful upgrade is not a larger ridge feature set. It should be:

1. A sparse/regularized router that can select regime features instead of always using all of them.
2. A walk-forward hyperparameter search with a validation-only tuning window.
3. Only after that, an LLM macro tag adapter.

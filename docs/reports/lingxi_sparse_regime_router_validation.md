# Lingxi Sparse Regime Router Validation

Date: 2026-06-23

## Objective

Test whether feature selection can reduce the noise introduced by the full market-regime router.

The previous experiment showed that market-regime features contain useful information, but the full feature set still loses to fixed/static baselines in most scenarios. This experiment adds a rolling feature-selection step before ridge fitting.

## Method

For each market/topk/variant/sleeve:

1. Build the same contextual + market-regime feature vector as the previous regime router.
2. Use only lagged data at least 5 trading days behind the decision date.
3. Rank features by absolute correlation with the sleeve's lagged reward inside the rolling training window.
4. Keep at most 20 non-intercept features.
5. Fit ridge on the selected feature subset.

Important limitation: this is better described as a **feature-capped regime router**, not a strongly sparse model. Diagnostics show it usually keeps about 19 of 20 allowed features.

## Protocol

| Item | Setting |
|---|---|
| Sample | 2023-01-03 to 2026 YTD |
| Source strategies | `experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/` |
| Markets | China A-share, US large cap, HK large cap, crypto major |
| TopK | 10, 5 |
| Variants | raw, industry/size neutral |
| New router | `sparse_regime_ridge_router` |
| Feature cap | 20 non-intercept features |
| Diagnostics | `*_diagnostics.csv` per scenario |
| Output | `experiments/lingxi_sparse_regime_router_validation_2026_ytd/` |

Reproduction:

```powershell
python scripts\run_lingxi_sparse_regime_router_validation.py --out-dir experiments\lingxi_sparse_regime_router_validation_2026_ytd
```

## Main Conclusion

Feature-capped regime routing is a modest improvement over the previous dynamic routers, but it still does not justify replacing the fixed/scene-specific production menu.

Evidence:

- Sparse/feature-capped regime beats the best fixed/static baseline in 3 of 16 scenarios.
- It beats full market-regime ridge in 8 of 16 scenarios.
- It beats the non-regime contextual ridge in 10 of 16 scenarios.
- The best new wins are A-share Top5 neutral, Crypto Top10 raw, and HK Top5 raw.
- Several losses remain severe, especially A-share raw, HK Top10, US neutral, and crypto neutral.

This confirms the research direction: routing benefits from controlled feature selection, but the edge is still too scenario-specific.

## Scenario Results

| Scenario | Best fixed/static | Ann. / Sharpe / MDD | Contextual ridge Sharpe | Full regime Sharpe | Sparse regime | Sparse wins fixed? |
|---|---|---:|---:|---:|---:|---|
| A-share Top10 raw | Static ensemble | 116.40% / 7.65 / -13.35% | 7.77 | 7.11 | 120.35% / 6.98 / -13.38% | No |
| A-share Top10 neutral | Lingxi | 100.75% / 5.86 / -23.57% | 5.62 | 5.95 | 86.17% / 5.77 / -16.20% | No |
| A-share Top5 raw | Static ensemble | 137.79% / 7.78 / -12.16% | 7.65 | 6.06 | 131.59% / 6.57 / -20.59% | No |
| A-share Top5 neutral | Lingxi | 130.65% / 6.17 / -25.46% | 6.06 | 6.20 | 122.09% / 6.78 / -26.27% | Yes |
| US Top10 raw | PITNorm | 49.52% / 6.11 / -11.60% | 5.83 | 5.76 | 52.04% / 6.07 / -13.94% | No |
| US Top10 neutral | Lingxi | 42.54% / 5.38 / -14.26% | 4.86 | 4.94 | 37.72% / 4.88 / -17.73% | No |
| US Top5 raw | Static ensemble | 64.11% / 6.76 / -12.21% | 5.58 | 5.81 | 61.90% / 6.10 / -13.40% | No |
| US Top5 neutral | Static ensemble | 48.69% / 5.69 / -16.36% | 5.19 | 5.11 | 49.27% / 5.29 / -19.11% | No |
| HK Top10 raw | PITNorm | 41.60% / 3.30 / -15.63% | 3.16 | 3.07 | 35.22% / 2.91 / -15.23% | No |
| HK Top10 neutral | PITNorm | 28.01% / 2.43 / -18.88% | 2.23 | 2.26 | 24.38% / 2.14 / -21.51% | No |
| HK Top5 raw | PITNorm | 45.98% / 3.47 / -14.38% | 3.40 | 3.32 | 48.79% / 3.58 / -15.06% | Yes |
| HK Top5 neutral | PITNorm | 33.28% / 2.58 / -21.17% | 2.23 | 2.39 | 30.09% / 2.27 / -16.52% | No |
| Crypto Top10 raw | ReturnFloor-Gate | 72.62% / 2.59 / -60.15% | 2.48 | 2.51 | 73.49% / 2.63 / -58.85% | Yes |
| Crypto Top10 neutral | Lingxi | 47.70% / 1.75 / -59.87% | 1.73 | 1.62 | 39.80% / 1.50 / -58.89% | No |
| Crypto Top5 raw | ReturnFloor-Gate | 128.98% / 3.45 / -58.91% | 3.24 | 3.60 | 129.21% / 3.38 / -59.33% | No |
| Crypto Top5 neutral | Lingxi | 79.08% / 2.21 / -62.04% | 2.23 | 1.77 | 77.05% / 2.20 / -61.67% | No |

## Diagnostics

Average selected non-intercept feature count is about 19 across all scenarios. That means the current configuration acts as a cap against the noisiest tail of features, not as aggressive sparsity.

This explains the mixed result:

- It repairs some full-regime overfitting.
- It does not create enough structure to beat fixed baselines broadly.
- It can still worsen drawdown when it chases short-window feature correlations.

## Decision

Promote these research sleeves:

| Sleeve | Decision |
|---|---|
| A-share Top5 neutral sparse regime | Keep as high-Sharpe research sleeve, but drawdown is not improved |
| Crypto Top10 raw sparse regime | Keep as research sleeve |
| HK Top5 raw sparse regime | Keep as research sleeve |

Reject as production:

- US sparse regime routers
- HK Top10 sparse regime routers
- Crypto neutral sparse regime routers
- A-share raw sparse regime routers

## LLM Implication

This strengthens the constraint on any LLM macro adapter:

1. LLM tags must be sparse, dated, and frozen before evaluation.
2. They must pass the same fixed/static baseline comparison, not merely improve over a weaker router.
3. Any LLM debate output should be audit/explanation unless its structured tags show out-of-sample lift.

## Next Step

The next useful experiment is a validation-only meta-selector:

- Do not force one router everywhere.
- Use a pre-2025 validation window to choose among fixed/static, contextual ridge, full regime, and sparse regime per scenario.
- Then evaluate that frozen scenario menu on 2025 and 2026 YTD.

This is closer to how the strategy should actually be deployed.

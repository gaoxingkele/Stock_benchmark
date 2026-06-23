# CASE-Lingxi Conservative Context Router Validation

Date: 2026-06-23

This report validates the first CASE-Lingxi router implementation:

```text
scripts/run_case_lingxi_context_router.py
```

The router is intentionally conservative. It only selects among already validated Lingxi-family sleeves:

1. `lingxi`
2. `lingxi_pitnorm`
3. `lingxi_pitnorm_gate_return_floor`

It does not trade individual stocks directly and does not use LLM outputs.

## Protocol

Input source:

```text
experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/
```

Output:

```text
experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv
```

Rows: 112

Markets:

1. China A-share
2. US large cap
3. HK large cap
4. Crypto major

Portfolio settings:

1. H5 label
2. Top10 and Top5
3. raw and industry/size neutral variants
4. equal-weight long-only
5. daily rebalance
6. single-side 10 bps cost inherited from the source daily files

## Router Design

The script compares:

1. `case_lingxi_static_menu`
2. `case_lingxi_context_router`
3. `static_equal_ensemble`
4. `oracle_upper_bound`
5. the three fixed sleeves

The static menu follows the current production decision:

| Market/scenario | Static menu sleeve |
|---|---|
| HK Top10/Top5 | PITNorm |
| Crypto raw | ReturnFloor-Gate |
| US Top10 | PITNorm |
| Other scenarios | Lingxi |

The context router starts from the static menu and switches only under lagged stress conditions:

1. 60-day drawdown below threshold;
2. 20-day volatility above trailing quantile;
3. moderate drawdown plus weak breadth.

When stressed, it chooses the best approved risk sleeve using lagged rolling risk-adjusted scores. A switch penalty discourages unnecessary sleeve churn.

## Result Versus Static Menu

Across 16 market/TopK/variant scenarios:

| Metric | Router wins | Interpretation |
|---|---:|---|
| Annualized return | 3 / 16 | Not a return upgrade |
| Sharpe | 3 / 16 | Not a broad risk-adjusted upgrade |
| MDD | 9 / 16 | Useful drawdown-control signal |

## Scenario Details

| Market | TopK | Variant | Router ann. | Menu ann. | Router Sharpe | Menu Sharpe | Router MDD | Menu MDD | Decision |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| China A-share | 10 | raw | 121.46% | 127.61% | 7.44 | 6.80 | -14.69% | -17.49% | research risk-control candidate |
| China A-share | 10 | neutral | 71.20% | 100.75% | 5.16 | 5.86 | -22.43% | -23.57% | reject as replacement |
| China A-share | 5 | raw | 131.05% | 161.96% | 6.83 | 6.96 | -16.45% | -26.14% | drawdown sleeve only |
| China A-share | 5 | neutral | 97.80% | 130.65% | 5.59 | 6.17 | -17.90% | -25.46% | drawdown sleeve only |
| US large cap | 10 | raw | 47.10% | 49.52% | 5.75 | 6.11 | -12.14% | -11.60% | reject as replacement |
| US large cap | 10 | neutral | 41.45% | 37.46% | 5.45 | 5.01 | -16.15% | -16.56% | narrow candidate |
| US large cap | 5 | raw | 65.45% | 69.14% | 6.15 | 6.40 | -15.89% | -18.39% | drawdown sleeve only |
| US large cap | 5 | neutral | 49.84% | 55.68% | 5.28 | 5.58 | -16.80% | -16.72% | reject |
| HK large cap | 10 | raw | 38.59% | 41.60% | 3.06 | 3.30 | -15.78% | -15.63% | reject |
| HK large cap | 10 | neutral | 26.67% | 28.01% | 2.26 | 2.43 | -19.61% | -18.88% | reject |
| HK large cap | 5 | raw | 47.40% | 45.98% | 3.42 | 3.47 | -14.43% | -14.38% | not enough |
| HK large cap | 5 | neutral | 29.85% | 33.28% | 2.28 | 2.58 | -19.96% | -21.17% | drawdown sleeve only |
| Crypto major | 10 | raw | 73.54% | 72.62% | 2.62 | 2.59 | -59.38% | -60.15% | narrow candidate |
| Crypto major | 10 | neutral | 36.47% | 47.70% | 1.38 | 1.75 | -60.26% | -59.87% | reject |
| Crypto major | 5 | raw | 118.57% | 128.98% | 3.24 | 3.45 | -57.77% | -58.91% | drawdown sleeve only |
| Crypto major | 5 | neutral | 71.96% | 79.08% | 2.08 | 2.21 | -64.31% | -62.04% | reject |

## Conclusion

The conservative context router is a useful **research sleeve**, not a production replacement.

It confirms the central CASE-Lingxi thesis:

1. constrained routing can reduce drawdown in many scenarios;
2. even conservative routing often sacrifices too much return or Sharpe;
3. the production default should remain the fixed scenario-specific Lingxi Adaptive Suite;
4. future RL or LLM routers must beat this conservative menu OOS before promotion.

## Reproduction

```powershell
python scripts\run_case_lingxi_context_router.py --out-dir experiments\case_lingxi_context_router_validation_2026_ytd
```

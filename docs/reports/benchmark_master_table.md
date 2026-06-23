# Benchmark Master Table

Date: 2026-06-23

This file is the current execution-level benchmark index for the Lingxi workstream. It does not replace the detailed reports; it points to the authoritative result artifacts and records the current production decision.

## Evidence Sources

| Evidence | Rows | Scope |
|---|---:|---|
| `experiments/lingxi_sota_upgrade_validation/lingxi_sota_upgrade_validation_summary.csv` | 96 | Lingxi10/Lingxi5 versus LinearGuard, PITNorm, MScale, Patch, and VarAttn across China A-share, US large cap, HK large cap, and crypto major |
| `experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/lingxi_pitnorm_tuned_gate_validation_summary.csv` | 64 | 2026 YTD fixed Lingxi/PITNorm/ReturnFloor evidence |
| `experiments/lingxi_adaptive_router_validation_2026_ytd/lingxi_adaptive_router_validation_summary.csv` | 128 | First adaptive router comparison |
| `experiments/lingxi_regime_router_validation_2026_ytd/lingxi_regime_router_validation_summary.csv` | 112 | Market-regime router comparison |
| `experiments/lingxi_sparse_regime_router_validation_2026_ytd/lingxi_sparse_regime_router_validation_summary.csv` | 128 | Sparse/feature-capped regime router comparison |
| `experiments/lingxi_meta_selector_validation/lingxi_meta_selector_validation_summary.csv` | 416 | Frozen validation-selector OOS failure evidence |
| `experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv` | 112 | Conservative CASE-Lingxi context-router validation |
| `experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv` | 128 | Frozen research-only RL router validation on 2025-2026 YTD OOS |
| `experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv` | 128 | Structured LLM-compatible market-tag ablation |
| `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv` | 3 | Unified candidate-vs-menu promotion audit with paired bootstrap intervals |
| `experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_summary.csv` | 15 | Candidate-vs-menu cost sensitivity at 0/5/10/20/50 bps |
| `data/ara_method_registry.csv` | 31 | Audited finance method registry with ARA and experiment-validation status |

## Scenario Winners From The SOTA Upgrade Run

The table below ranks by Sharpe within each market, TopK, and variant scenario. Return and drawdown are still used in the final production decision, because the highest Sharpe sleeve is not always the best production sleeve.

| Market | TopK | Variant | Best Sharpe method | Ann. return | Sharpe | MDD | Cum. return | Decision |
|---|---:|---|---|---:|---:|---:|---:|---|
| China A-share | 10 | raw | `lingxi_pitnorm` | 96.89% | 6.78 | -12.20% | 605.98% | risk-control candidate; Lingxi keeps return edge |
| China A-share | 10 | neutral | `lingxi` | 89.65% | 5.15 | -23.57% | 533.68% | keep Lingxi |
| China A-share | 5 | raw | `lingxi_pitnorm` | 119.28% | 7.29 | -12.35% | 863.33% | strong risk-control candidate |
| China A-share | 5 | neutral | `lingxi` | 116.66% | 5.50 | -25.46% | 830.45% | keep Lingxi |
| US large cap | 10 | raw | `lingxi_pitnorm` | 46.23% | 6.14 | -11.50% | 210.83% | risk-control candidate |
| US large cap | 10 | neutral | `lingxi_pitnorm` | 40.72% | 5.71 | -14.04% | 177.16% | risk-control candidate |
| US large cap | 5 | raw | `lingxi` | 61.33% | 6.09 | -18.39% | 316.72% | keep Lingxi |
| US large cap | 5 | neutral | `lingxi` | 51.26% | 5.70 | -14.74% | 243.82% | keep Lingxi |
| HK large cap | 10 | raw | `lingxi_pitnorm` | 46.21% | 3.49 | -15.63% | 202.81% | use PITNorm |
| HK large cap | 10 | neutral | `lingxi_pitnorm` | 31.42% | 2.60 | -18.88% | 121.88% | use PITNorm |
| HK large cap | 5 | raw | `lingxi_pitnorm` | 51.17% | 3.68 | -14.38% | 233.77% | use PITNorm |
| HK large cap | 5 | neutral | `lingxi_pitnorm` | 36.56% | 2.74 | -21.17% | 148.13% | use PITNorm |
| Crypto major | 10 | raw | `lingxi` | 108.61% | 3.73 | -41.94% | 2333.94% | keep Lingxi/ReturnFloor-gated production sleeve |
| Crypto major | 10 | neutral | `lingxi` | 72.57% | 2.56 | -45.06% | 968.48% | keep Lingxi or PITNorm only after risk gate |
| Crypto major | 5 | raw | `lingxi` | 192.32% | 4.77 | -43.75% | 10429.74% | keep Lingxi/ReturnFloor-gated production sleeve |
| Crypto major | 5 | neutral | `lingxi` | 121.12% | 3.21 | -40.67% | 3033.99% | keep Lingxi |

## Average Method Ranking

Across the 16 SOTA-upgrade scenarios:

| Method | Scenarios | Average annualized return | Average Sharpe | Average MDD | Interpretation |
|---|---:|---:|---:|---:|---|
| `lingxi_pitnorm` | 16 | 69.72% | 4.50 | -21.72% | best average Sharpe and drawdown; often sacrifices return |
| `lingxi` | 16 | 83.00% | 4.48 | -25.15% | best practical default; strongest return edge |
| `lingxi_linear_guard` | 16 | 30.48% | 1.55 | -38.62% | useful guardrail, not a replacement |
| `lingxi_mscale` | 16 | 28.32% | 1.46 | -37.24% | rejected as first-pass replacement |
| `lingxi_patch` | 16 | 21.98% | 1.35 | -38.03% | rejected as first-pass replacement |
| `lingxi_varattn` | 16 | 9.01% | 0.49 | -38.67% | cheap proxy rejected; does not reject a full iTransformer implementation |

## Current Production Decision

The best current production form is still **Lingxi Adaptive Suite**, meaning a conservative menu rather than a universal router.

Production defaults:

1. A-share Top10/Top5: Lingxi, with PITNorm as a risk-control candidate for raw portfolios.
2. US large cap Top10: PITNorm may be used as risk control; US Top5 remains Lingxi.
3. HK Top10/Top5: PITNorm.
4. Crypto Top10/Top5: Lingxi or ReturnFloor-gated Lingxi for raw portfolios; do not use a production dynamic router yet.

Rejected production routes:

1. Validation-Sharpe meta-selector.
2. Universal adaptive router.
3. Direct LLM trading router.
4. Unvalidated fixed fusion of generic SOTA proxy features.

New router evidence:

1. CASE-Lingxi conservative context router wins annualized return in 3/16 scenarios versus the static production menu.
2. It wins Sharpe in 3/16 scenarios.
3. It improves MDD in 9/16 scenarios.
4. It is therefore a drawdown-control research sleeve, not a production replacement.
5. CASE-Lingxi frozen tabular RL router wins annualized return in 4/16 scenarios, Sharpe in 4/16, and MDD in 6/16 on 2025-2026 YTD OOS.
6. The RL router is also research-only and does not supersede the static menu.
7. CASE-Lingxi structured market-tag router wins annualized return in 0/16, Sharpe in 2/16, and MDD in 7/16 versus the static menu.
8. LLM-compatible tags are therefore an audit/context interface, not a production routing signal yet.
9. The unified promotion audit finds zero candidates with any positive annualized daily-return difference bootstrap lower-bound wins.
10. The cost sensitivity audit finds no candidate reaches the production gate at 0, 5, 10, 20, or 50 bps.

## Next Benchmarks To Run

1. Re-run Lingxi10/Lingxi5 plus PITNorm on 2026 YTD with the same table shape as the 2023-2025 SOTA upgrade report.
2. Expand the ARA trace with earlier sparse-regime, market-regime, and SOTA-proxy branches.
3. Upgrade paper related work with BibTeX-backed citations.

# Experiments

## Protocol

Markets:

1. China A-share
2. US large cap
3. HK large cap
4. Crypto major

Portfolio settings:

1. H5 forward return label;
2. Top10 and Top5 portfolios;
3. raw and industry/size neutral variants where meaningful;
4. equal-weight long-only;
5. daily rebalance;
6. single-side 10 bps transaction cost.

## Evidence Index

| Experiment | Script | Summary artifact | Rows |
|---|---|---|---:|
| Lingxi SOTA upgrade | `scripts/run_lingxi_sota_upgrade_validation.py` | `experiments/lingxi_sota_upgrade_validation/lingxi_sota_upgrade_validation_summary.csv` | 96 |
| Context router | `scripts/run_case_lingxi_context_router.py` | `experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv` | 112 |
| Frozen RL router | `scripts/run_case_lingxi_rl_router_baseline.py` | `experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv` | 128 |
| Market-tag ablation | `scripts/run_case_lingxi_llm_tag_ablation.py` | `experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv` | 128 |
| Validation-only selector | `scripts/run_lingxi_meta_selector_validation.py` | `experiments/lingxi_meta_selector_validation/lingxi_meta_selector_validation_summary.csv` | 416 |
| Promotion audit | `scripts/run_case_lingxi_promotion_audit.py` | `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv` | 3 |

## Main Results

### Promotion Audit

The unified promotion audit recomputes candidate-vs-menu daily differences and adds block-bootstrap confidence intervals. No adaptive candidate has any scenario where the annualized daily-return difference bootstrap lower bound is positive.

| Candidate | Ann. wins | Sharpe wins | MDD wins | Positive annualized-diff CI wins |
|---|---:|---:|---:|---:|
| Conservative context router | 3 / 16 | 4 / 16 | 9 / 16 | 0 / 16 |
| Frozen tabular RL router | 4 / 16 | 4 / 16 | 6 / 16 | 0 / 16 |
| Structured market-tag router | 1 / 16 | 3 / 16 | 7 / 16 | 0 / 16 |

This is the strictest current evidence against production promotion of the adaptive candidates.

### Conservative Context Router

Versus the static production menu:

| Metric | Wins |
|---|---:|
| Annualized return | 3 / 16 |
| Sharpe | 3 / 16 |
| MDD | 9 / 16 |

Interpretation: useful drawdown-control research sleeve, not a production replacement.

### Frozen Tabular RL Router

Versus the static production menu on 2025-2026 YTD OOS:

| Metric | Wins |
|---|---:|
| Annualized return | 4 / 16 |
| Sharpe | 4 / 16 |
| MDD | 6 / 16 |

Interpretation: research-only negative control.

### Structured Market-Tag Router

Versus the static production menu:

| Metric | Wins |
|---|---:|
| Annualized return | 0 / 16 |
| Sharpe | 2 / 16 |
| MDD | 7 / 16 |

Interpretation: market tags are useful as an audit/context interface, but not a production signal yet.

### Validation Echo Trap

The validation-only Sharpe selector wins:

| Window | Wins |
|---|---:|
| 2025 | 2 / 16 |
| 2026 YTD | 0 / 16 |
| Combined 2025-2026 YTD | 1 / 16 |

Interpretation: validation-only selection is rejected.

## Reproduction Commands

```powershell
python scripts\run_lingxi_sota_upgrade_validation.py --out-dir experiments\lingxi_sota_upgrade_validation
python scripts\run_case_lingxi_context_router.py --out-dir experiments\case_lingxi_context_router_validation_2026_ytd
python scripts\run_case_lingxi_rl_router_baseline.py --out-dir experiments\case_lingxi_rl_router_validation_2025_2026_ytd
python scripts\run_case_lingxi_llm_tag_ablation.py --out-dir experiments\case_lingxi_llm_tag_ablation_2026_ytd
python scripts\run_lingxi_meta_selector_validation.py --out-dir experiments\lingxi_meta_selector_validation
python scripts\run_case_lingxi_promotion_audit.py --out-dir experiments\case_lingxi_promotion_audit
```

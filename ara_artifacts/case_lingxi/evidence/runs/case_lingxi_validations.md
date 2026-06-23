# CASE-Lingxi Validation Runs

## Benchmark Master

- Summary file: `experiments/lingxi_sota_upgrade_validation/lingxi_sota_upgrade_validation_summary.csv`
- Rows: 96
- Main conclusion: Lingxi remains the main production anchor; PITNorm is useful as risk control.

## Conservative Context Router

- Script: `scripts/run_case_lingxi_context_router.py`
- Summary file: `experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv`
- Rows: 112
- Result versus static menu:
  - annualized return wins: 3/16
  - Sharpe wins: 3/16
  - MDD wins: 9/16
- Decision: research-only drawdown sleeve.

## Frozen Tabular RL Router

- Script: `scripts/run_case_lingxi_rl_router_baseline.py`
- Summary file: `experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv`
- Rows: 128
- Training: 2023-2024
- OOS: 2025-2026 YTD
- Result versus static menu:
  - annualized return wins: 4/16
  - Sharpe wins: 4/16
  - MDD wins: 6/16
- Decision: research-only negative control.

## Structured Market-Tag Ablation

- Script: `scripts/run_case_lingxi_llm_tag_ablation.py`
- Summary file: `experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv`
- Rows: 128
- Tag schema: `case_lingxi_market_tags_v1`
- Result versus static menu:
  - annualized return wins: 0/16
  - Sharpe wins: 2/16
  - MDD wins: 7/16
- Decision: market tags are audit/context interface only.

## Validation-Only Meta-Selector

- Script: `scripts/run_lingxi_meta_selector_validation.py`
- Summary file: `experiments/lingxi_meta_selector_validation/lingxi_meta_selector_validation_summary.csv`
- Rows: 416
- Result:
  - 2025 wins: 2/16
  - 2026 YTD wins: 0/16
  - combined wins: 1/16
- Decision: rejected; named validation echo trap.

## Unified Promotion Audit

- Script: `scripts/run_case_lingxi_promotion_audit.py`
- Summary file: `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv`
- Detail file: `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_detail.csv`
- Rows:
  - summary: 3
  - detail: 48
- Result:
  - context router positive annualized-diff CI wins: 0/16
  - RL router positive annualized-diff CI wins: 0/16
  - market-tag router positive annualized-diff CI wins: 0/16
- Decision: no adaptive candidate passes production gate.

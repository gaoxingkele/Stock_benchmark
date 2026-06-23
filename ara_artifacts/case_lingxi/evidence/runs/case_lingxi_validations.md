# CASE-Lingxi Validation Runs

## Benchmark Master

- Summary file: `experiments/lingxi_sota_upgrade_validation/lingxi_sota_upgrade_validation_summary.csv`
- Rows: 96
- Main conclusion: Lingxi remains the main production anchor; PITNorm is useful as risk control.

## Prior Router Branches

These branches are included in the exploration trace because they shaped the final static-menu decision:

| Branch | Report | Summary artifact | Decision |
|---|---|---|---|
| Adaptive router | `docs/reports/lingxi_adaptive_router_validation.md` | `experiments/lingxi_adaptive_router_validation_2026_ytd/lingxi_adaptive_router_validation_summary.csv` | rejected as global production default |
| Market-regime router | `docs/reports/lingxi_regime_router_validation.md` | `experiments/lingxi_regime_router_validation_2026_ytd/lingxi_regime_router_validation_summary.csv` | rejected as global production default |
| Sparse regime router | `docs/reports/lingxi_sparse_regime_router_validation.md` | `experiments/lingxi_sparse_regime_router_validation_2026_ytd/lingxi_sparse_regime_router_validation_summary.csv` | rejected as global production default |
| SOTA/PITNorm upgrade | `docs/reports/lingxi_sota_upgrade_validation.md` | `experiments/lingxi_sota_upgrade_validation/lingxi_sota_upgrade_validation_summary.csv` | PITNorm kept as risk-control candidate |

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
  - context router positive Sharpe-diff CI wins: 0/16
  - context router positive MDD-diff CI wins: 0/16
  - RL router positive annualized-diff CI wins: 0/16
  - RL router positive Sharpe-diff CI wins: 0/16
  - RL router positive MDD-diff CI wins: 0/16
  - market-tag router positive annualized-diff CI wins: 0/16
  - market-tag router positive Sharpe-diff CI wins: 0/16
  - market-tag router positive MDD-diff CI wins: 0/16
- Decision: no adaptive candidate passes production gate.

## Cost Sensitivity Audit

- Script: `scripts/run_case_lingxi_cost_sensitivity.py`
- Summary file: `experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_summary.csv`
- Detail file: `experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_detail.csv`
- Rows:
  - summary: 15
  - detail: 240
- Cost levels: 0, 5, 10, 20, 50 bps
- Result: no adaptive candidate passes production gate at any tested cost level.
- Decision: static production menu remains default; context router remains risk-control candidate only.

## Capacity and Slippage Stress Audit

- Script: `scripts/run_case_lingxi_capacity_slippage.py`
- Summary file: `experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_summary.csv`
- Detail file: `experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_detail.csv`
- Rows:
  - summary: 60
  - detail: 960
- Stress model:
  - linear cost: 10 bps
  - AUM multipliers: 0.5, 1, 2, 5, 10
  - nonlinear impact bps: 0, 5, 10, 20
- Result:
  - context router max annualized wins: 3/16; max Sharpe wins: 5/16; max MDD wins: 10/16
  - RL router max annualized wins: 6/16; max Sharpe wins: 5/16; max MDD wins: 6/16
  - market-tag router max annualized wins: 2/16; max Sharpe wins: 3/16; max MDD wins: 8/16
- Decision: nonlinear capacity/slippage stress does not promote any adaptive candidate.

## Citation Coverage Audit

- Script: `scripts/validate_case_lingxi_citations.py`
- Coverage file: `papers/metadata/case_lingxi_citation_coverage.csv`
- BibTeX file: `papers/metadata/references.bib`
- Recovery scripts:
  - `scripts/build_case_lingxi_draft_bib.py`
  - `scripts/extract_case_lingxi_missing_citation_metadata.py`
- Result:
  - finance registry rows: 31
  - coverage rows: 31
  - BibTeX keys: 35
  - finance-registry citations added: 31
  - pending finance-registry citations: 0
- Decision: 31-method finance registry and current related-work citation coverage are complete; remaining citation work is venue-template-specific formatting.

## Level 2 Rigor Review Refresh

- Report file: `ara_artifacts/case_lingxi/level2_report.json`
- Review date: 2026-06-23
- Grade: Accept
- Mean score: 4.0
- Main resolved prior weaknesses:
  - Sharpe and MDD bootstrap intervals added to promotion audit
  - nonlinear capacity/slippage stress added
  - 31-method BibTeX coverage completed
  - additional time-series SOTA, foundation-model, multi-agent debate, and collaborative LLM-RL citations added
- Remaining limitations:
  - no live timestamped LLM-debate tag experiment yet
  - no calibrated real-market ADV/liquidity capacity model
  - trace provenance/timestamps are not fully reconstructed

## Bundle Validation

- Script: `scripts/validate_case_lingxi_bundle.py`
- Checks:
  - CASE-Lingxi summary/detail CSV row counts
  - citation coverage validation
  - BibTeX hygiene validation
  - ARA Level 1 structural validation
- Current result: `CASE_LINGXI_BUNDLE_VALIDATION_PASS`

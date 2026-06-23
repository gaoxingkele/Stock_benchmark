# CASE-Lingxi Completion Audit

Date: 2026-06-23

This audit checks whether the actionable CASE-Lingxi execution plan is complete from committed repository evidence.

## Validation Command

```powershell
python scripts\validate_case_lingxi_bundle.py
```

Current result:

```text
CASE_LINGXI_BUNDLE_VALIDATION_PASS
```

## Requirement Audit

| Requirement | Evidence | Status |
|---|---|---|
| Lock benchmark baseline and 31-method registry | `docs/reports/benchmark_master_table.md`, `data/ara_method_registry.csv`, `papers/metadata/case_lingxi_citation_coverage.csv` | complete |
| Index current Lingxi/PITNorm/Lingxi5/Lingxi10 evidence | `PROJECT_MEMORY.md`, `docs/reports/benchmark_master_table.md`, `experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/lingxi_pitnorm_tuned_gate_validation_summary.csv` | complete |
| Record rejected dynamic routers and meta-selector failures | `docs/reports/lingxi_adaptive_router_validation.md`, `docs/reports/lingxi_regime_router_validation.md`, `docs/reports/lingxi_sparse_regime_router_validation.md`, `docs/reports/lingxi_meta_selector_validation.md` | complete |
| Connect Lingxi to agentic RL / agent-evolution literature | `docs/literature/agent_rl_strategy_evolution_survey.md`, `paper/related_work.md`, `papers/metadata/references.bib` | complete |
| Formulate conservative agentic strategy-evolution theory | `docs/theory/case_lingxi_framework.md`, `docs/theory/case_lingxi_promotion_gate.md`, `paper/formulation.md` | complete |
| Implement conservative context router | `scripts/run_case_lingxi_context_router.py`, `experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv`, `docs/reports/case_lingxi_context_router_validation.md` | complete |
| Implement frozen research-only RL router | `scripts/run_case_lingxi_rl_router_baseline.py`, `experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv`, `docs/reports/case_lingxi_rl_router_validation.md` | complete |
| Implement structured LLM-compatible market-tag ablation | `scripts/run_case_lingxi_llm_tag_ablation.py`, `experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv`, `docs/reports/case_lingxi_llm_tag_ablation.md` | complete |
| Create paper draft | `paper/outline.md`, `paper/abstract.md`, `paper/introduction.md`, `paper/method.md`, `paper/experiments.md`, `paper/related_work.md`, `paper/formulation.md`, `paper/citation_map.md` | complete draft |
| Add full citation coverage | `papers/metadata/references.bib`, `scripts/validate_case_lingxi_citations.py`, `scripts/validate_references_bib.py` | complete |
| Upgrade to ARA package | `ara_artifacts/case_lingxi/`, `ara_artifacts/case_lingxi/level2_report.json` | complete |
| Validate ARA Level 1 | `python C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py ara_artifacts/case_lingxi` | pass |
| Run Level 2 rigor review | `ara_artifacts/case_lingxi/level2_report.json` | Accept |
| Add promotion audit with bootstrap statistics | `scripts/run_case_lingxi_promotion_audit.py`, `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv` | complete |
| Add cost sensitivity audit | `scripts/run_case_lingxi_cost_sensitivity.py`, `experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_summary.csv` | complete |
| Add nonlinear capacity/slippage stress | `scripts/run_case_lingxi_capacity_slippage.py`, `experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_summary.csv` | complete |
| Provide one-command bundle validation | `scripts/validate_case_lingxi_bundle.py` | complete |
| Push repository state to GitHub | `origin/main` at or after this report commit | complete after push |

## Bundle Validation Scope

`scripts/validate_case_lingxi_bundle.py` verifies:

1. row counts for CASE-Lingxi summary/detail CSV files;
2. 31/31 finance-registry citation coverage;
3. 46-entry BibTeX hygiene;
4. ARA Level 1 structural validity.

## Current Production Conclusion

The final validated scheme remains **Lingxi Adaptive Suite**:

1. use conservative fixed/scenario-specific sleeves for production;
2. keep context router as a risk-control research sleeve;
3. keep frozen tabular RL router and market-tag router as negative controls;
4. do not let LLMs or RL directly route production trades without frozen OOS promotion evidence.

## Non-Blocking Future Work

The following are future research or manuscript-polish items, not blockers for the completed CASE-Lingxi bundle:

1. choose a target venue/template and polish the manuscript accordingly;
2. add trace provenance timestamps if a full research-process reconstruction is needed;
3. run a future frozen timestamped LLM-debate tag experiment;
4. calibrate capacity/slippage with real ADV/liquidity data if live-trading readiness becomes a claim.

## Audit Decision

The actionable CASE-Lingxi execution plan is complete under the current repository scope. Future work is explicitly scoped as optional or dependent on new external data/venue choices.

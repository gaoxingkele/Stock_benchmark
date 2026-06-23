# Project Memory: Stock Benchmark

Last updated: 2026-06-23

Repository:

```text
https://github.com/gaoxingkele/Stock_benchmark
```

Current restored state:

```text
main @ latest local branch state after CASE-Lingxi planning documents
```

## Final Best Scheme

The best validated scheme is **Lingxi Adaptive Suite**.

This is not a single universal dynamic router. The final conclusion is a conservative strategy suite:

1. Use fixed/scene-specific sleeves for production.
2. Keep dynamic routers only as research sleeves.
3. Do not use validation-Sharpe winner selection as a production meta-selector.
4. Do not let LLMs directly route trades; use LLMs only as structured macro tag adapters or audit/explanation tools.

## Production Menu

| Market | Scenario | Production proxy |
|---|---|---|
| China A-share | raw Top10/Top5 | Lingxi |
| China A-share | neutral Top10/Top5 | Lingxi |
| US large cap | Top10/Top5 | Fixed/static baselines: PITNorm, ReturnFloor-Gate, static ensemble, or Lingxi depending scenario |
| HK large cap | Top10/Top5 | PITNorm |
| Crypto major | raw Top10/Top5 | ReturnFloor-Gate |
| Crypto major | neutral Top10/Top5 | Lingxi or PITNorm |

## Research Sleeves

Keep these for further research, not production default:

- A-share Top5 neutral sparse regime
- Crypto Top10 raw sparse regime
- Crypto Top5 raw market-regime ridge
- HK Top5 raw sparse regime
- A-share Top10 raw contextual ridge

## Rejected Routes

| Route | Reason |
|---|---|
| Universal adaptive router | Too few wins vs fixed/static baselines |
| Full market-regime router everywhere | Adds signal but also adds noise |
| Sparse regime router everywhere | Better than some routers, but only 3/16 wins vs fixed/static |
| Validation-only Sharpe meta-selector | 2025: 2/16 wins; 2026 YTD: 0/16; combined: 1/16 |
| Direct LLM trading router | Not reproducible enough and not validated out of sample |

## Core Validation Evidence

Experiment summaries:

| Artifact | Expected row count | Meaning |
|---|---:|---|
| `experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/lingxi_pitnorm_tuned_gate_validation_summary.csv` | 64 | Fixed Lingxi/PITNorm/ReturnFloor 2026 YTD source |
| `experiments/lingxi_adaptive_router_validation_2026_ytd/lingxi_adaptive_router_validation_summary.csv` | 128 | First adaptive router comparison |
| `experiments/lingxi_regime_router_validation_2026_ytd/lingxi_regime_router_validation_summary.csv` | 112 | Market-regime router comparison |
| `experiments/lingxi_sparse_regime_router_validation_2026_ytd/lingxi_sparse_regime_router_validation_summary.csv` | 128 | Sparse/feature-capped router comparison |
| `experiments/lingxi_meta_selector_validation/lingxi_meta_selector_selection_table.csv` | 16 | Frozen validation selections |
| `experiments/lingxi_meta_selector_validation/lingxi_meta_selector_validation_summary.csv` | 416 | Validation/OOS meta-selector comparison |
| `experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv` | 112 | Conservative CASE-Lingxi context-router validation |
| `experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv` | 128 | Frozen research-only RL router validation |
| `experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv` | 128 | Structured LLM-compatible market-tag ablation |
| `experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_summary.csv` | 60 | Nonlinear capacity/slippage stress audit |

Final reports:

- `docs/strategies/lingxi_adaptive_suite.md`
- `docs/strategies/lingxi_adaptive_router.md`
- `docs/reports/benchmark_master_table.md`
- `docs/theory/case_lingxi_framework.md`
- `docs/theory/case_lingxi_promotion_gate.md`
- `docs/design/case_lingxi_execution_plan.md`
- `docs/literature/agent_rl_strategy_evolution_survey.md`
- `data/ara_method_registry.csv`
- `docs/reports/lingxi_adaptive_router_validation.md`
- `docs/reports/lingxi_regime_router_validation.md`
- `docs/reports/lingxi_sparse_regime_router_validation.md`
- `docs/reports/lingxi_meta_selector_validation.md`
- `docs/reports/case_lingxi_context_router_validation.md`
- `docs/reports/case_lingxi_rl_router_validation.md`
- `docs/reports/case_lingxi_llm_tag_ablation.md`
- `docs/reports/case_lingxi_promotion_audit.md`
- `docs/reports/case_lingxi_cost_sensitivity.md`
- `docs/reports/case_lingxi_capacity_slippage.md`
- `docs/reports/case_lingxi_completion_audit.md`
- `docs/reports/wq_alpha_evolution_comparison_plan.md`
- `docs/reports/functionevolve_lingxi_feedback.md`
- `docs/reports/lingxi_functionevolve_blend.md`
- `docs/reports/lingxi_functionevolve_expanded.md`
- `docs/reports/wq_private_run_entrypoint.md`
- `docs/reports/wq_alpha_evolution_completion_audit.md`
- `ara_artifacts/case_lingxi/PAPER.md`
- `ara_artifacts/wq_alpha_evolution/PAPER.md`
- `paper/outline.md`
- `paper/abstract.md`
- `paper/introduction.md`
- `paper/method.md`
- `paper/experiments.md`
- `paper/citation_map.md`
- `docs/literature/case_lingxi_citation_coverage.md`

Core scripts:

- `scripts/run_lingxi_pitnorm_tuned_gate_validation.py`
- `scripts/run_lingxi_adaptive_router_validation.py`
- `scripts/run_lingxi_regime_router_validation.py`
- `scripts/run_lingxi_sparse_regime_router_validation.py`
- `scripts/run_lingxi_meta_selector_validation.py`
- `scripts/run_case_lingxi_context_router.py`
- `scripts/run_case_lingxi_rl_router_baseline.py`
- `scripts/run_case_lingxi_llm_tag_ablation.py`
- `scripts/run_case_lingxi_promotion_audit.py`
- `scripts/run_case_lingxi_cost_sensitivity.py`
- `scripts/run_case_lingxi_capacity_slippage.py`
- `scripts/validate_case_lingxi_bundle.py`
- `scripts/validate_wq_alpha_evolution_bundle.py`
- `scripts/run_wq_functionevolve_proxy.py`
- `scripts/run_lingxi_functionevolve_blend.py`
- `scripts/validate_sanitized_wq_run.py`

## Reproduction Commands

```powershell
python scripts\run_lingxi_pitnorm_tuned_gate_validation.py --test-end 2026-06-18 --out-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd
python scripts\run_lingxi_adaptive_router_validation.py --source-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd --out-dir experiments\lingxi_adaptive_router_validation_2026_ytd
python scripts\run_lingxi_regime_router_validation.py --out-dir experiments\lingxi_regime_router_validation_2026_ytd
python scripts\run_lingxi_sparse_regime_router_validation.py --out-dir experiments\lingxi_sparse_regime_router_validation_2026_ytd
python scripts\run_lingxi_meta_selector_validation.py --out-dir experiments\lingxi_meta_selector_validation
python scripts\validate_case_lingxi_bundle.py
python scripts\validate_wq_alpha_evolution_bundle.py
```

## Recovery Checklist

After cloning on another machine:

1. Confirm branch and commit:

```powershell
git status -sb
git log --oneline -5
```

2. Read:

```text
README.md
PROJECT_MEMORY.md
docs/strategies/lingxi_adaptive_suite.md
```

3. Confirm existing summary artifacts have the expected row counts listed above.

4. Treat `Lingxi Adaptive Suite` as the current best scheme unless new out-of-sample evidence supersedes it.

## Completed Goal: CASE-Lingxi

The expanded objective was to execute the CASE-Lingxi research plan:

1. lock the benchmark baseline and 31-method registry;
2. connect Lingxi to recent agentic RL / agent-evolution literature;
3. formulate the paper theory around conservative agentic strategy evolution;
4. implement conservative context routing, research-only RL routing, and LLM tag ablations;
5. upgrade the work into a CASE-Lingxi ARA package and paper draft.

Key principle:

Agents should improve the research loop, not directly route trades. Production promotion still requires frozen out-of-sample evidence against the conservative fixed/static menu.

First CASE-Lingxi router result:

- Conservative context router versus static production menu: annualized return wins 3/16, Sharpe wins 3/16, MDD wins 9/16.
- Interpretation: useful drawdown-control research sleeve, not a production replacement.

First CASE-Lingxi RL router result:

- Frozen tabular RL router trained on 2023-2024 and tested on 2025-2026 YTD: annualized return wins 4/16, Sharpe wins 4/16, MDD wins 6/16 versus the static production menu.
- Interpretation: research-only negative control; does not supersede the static menu.

First CASE-Lingxi LLM-compatible tag result:

- Structured market-tag router versus static production menu: annualized return wins 0/16, Sharpe wins 2/16, MDD wins 7/16.
- Interpretation: market tags are useful as a frozen audit/context interface, but not a production routing signal yet.

CASE-Lingxi ARA:

- Artifact path: `ara_artifacts/case_lingxi/`
- Level 1 structural validation: PASS with no warnings on 2026-06-23.
- Validation command: `python C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py ara_artifacts/case_lingxi`
- Bundle validation command: `python scripts\validate_case_lingxi_bundle.py`

CASE-Lingxi paper draft:

- Draft path: `paper/`
- Current files: `outline.md`, `abstract.md`, `introduction.md`, `method.md`, `experiments.md`, `related_work.md`, `formulation.md`, `citation_map.md`.
- The draft intentionally frames routers, RL, and LLM tags as negative or research-only evidence unless they beat the static menu OOS.
- Core BibTeX entries are in `papers/metadata/references.bib`; full 31-method citation pass is complete.
- 31-method citation coverage is tracked in `papers/metadata/case_lingxi_citation_coverage.csv`.
- Citation coverage validation command: `python scripts\validate_case_lingxi_citations.py`; current result is PASS with 31 added and 0 pending finance-registry entries.
- BibTeX hygiene validation command: `python scripts\validate_references_bib.py`; current result is PASS with 46 entries, 46 keys, no duplicate keys, no draft markers, and protected method-name capitalization.
- Draft BibTeX generation command: `python scripts\build_case_lingxi_draft_bib.py`; current result is 0 draft entries and no missing registry metadata rows.
- Missing-registry ARA metadata recovery command: `python scripts\extract_case_lingxi_missing_citation_metadata.py`; current result is 0 recovery rows because no finance-registry rows remain pending.
- Recovery output path: `papers/metadata/references_missing_metadata_from_ara.csv`.
- The 31 finance-registry citation entries and additional SOTA/agent references have been checked and promoted into `references.bib`; method-name capitalization is protected. Venue-specific bibliography polishing should wait until a target manuscript template is selected.

CASE-Lingxi completion audit:

- Report path: `docs/reports/case_lingxi_completion_audit.md`
- Bundle validation command: `python scripts\validate_case_lingxi_bundle.py`
- Current result: `CASE_LINGXI_BUNDLE_VALIDATION_PASS`

CASE-Lingxi Level 2 ARA review:

- Report path: `ara_artifacts/case_lingxi/level2_report.json`
- Overall grade: Accept
- Promotion audit now exists: `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv`
- Promotion audit includes paired block-bootstrap CI checks for annualized daily-return difference, Sharpe difference, and MDD difference; no adaptive candidate has a positive lower-bound CI win on any of the three metrics.
- Cost sensitivity now exists: `experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_summary.csv`
- Capacity/slippage stress now exists: `experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_summary.csv`; no adaptive candidate is promoted under the nonlinear stress grid.
- Main remaining improvement: optional venue-specific manuscript polish after selecting a target venue/template.

## Active Goal: WQ Alpha Evolution Comparison

The current objective is to complete the comparison-experiment plan for the open-source WorldQuant-style self-evolving factor-mining skill and the existing CASE-Lingxi benchmark.

Current artifact:

- ARA path: `ara_artifacts/wq_alpha_evolution/`
- Plan report: `docs/reports/wq_alpha_evolution_comparison_plan.md`
- FunctionEvolve feedback report: `docs/reports/functionevolve_lingxi_feedback.md`
- Current comparison table: `ara_artifacts/wq_alpha_evolution/evidence/current_cross_framework_comparison.csv`
- Public proxy result: `experiments/wq_functionevolve_proxy/functionevolve_proxy_summary.csv`
- Lingxi blend result: `experiments/lingxi_functionevolve_blend/lingxi_functionevolve_blend_summary.csv`
- Expanded proxy result: `experiments/wq_functionevolve_proxy_expanded/functionevolve_proxy_summary.csv`
- Expanded blend result: `experiments/lingxi_functionevolve_blend_expanded/lingxi_functionevolve_blend_summary.csv`
- Private WQ entrypoint: `docs/reports/wq_private_run_entrypoint.md`
- Completion audit: `docs/reports/wq_alpha_evolution_completion_audit.md`
- Bundle validation command: `python scripts\validate_wq_alpha_evolution_bundle.py`

Current scope:

1. Treat `QuantML-Research/wq-alpha-research` as an external open-source engineering reference for self-evolving alpha discovery.
2. Build a separate ARA protocol instead of mixing raw WorldQuant outputs into Lingxi.
3. Compare at the correct layer: alpha-discovery loop efficiency, ARA reproducibility, and CASE-Lingxi strategy-level OOS validation.
4. Exclude credentials, cookies, alpha IDs, raw private expressions, and raw PnL from the public repository.
5. Use sanitized aggregate schemas for any future private WorldQuant run.
6. Use FunctionEvolve-style AST factor evolution as the first public proxy factor-mining experiment.
7. Use SIA/Godel-Agent ideas only for the research harness, not direct trading, until frozen OOS evidence supports promotion.

Current status:

- Independent ARA scaffold exists.
- Sanitized WQ run schema exists.
- Public proxy factor-mining schema exists.
- Cross-framework comparison schema exists.
- Current layer-aware comparison table exists with 7 framework rows.
- FunctionEvolve-style public proxy run exists: 18 AST candidates, 18 valid factors, 1 promoted research-only factor.
- Current proxy run command: `python scripts\run_wq_functionevolve_proxy.py --max-candidates 18 --promotion-top 5 --max-symbols 25`
- Current proxy interpretation: the AST factor evolution loop is wired and reproducible, but the promoted factor is research-only because drawdown remains severe and the run is smoke-scale.
- Lingxi-FunctionEvolve-Memory smoke ablation exists: raw Lingxi5/Lingxi10 improved, neutral variants are mixed and only improve at low blend weight.
- Current blend command: `python scripts\run_lingxi_functionevolve_blend.py --max-symbols 80 --max-train-rows 50000`
- Expanded local evolution exists: 80-symbol FunctionEvolve-style proxy promotes 2 AST factors, then 0.15 blend improves raw Lingxi5/Lingxi10 and neutral Lingxi5.
- Expanded report: `docs/reports/lingxi_functionevolve_expanded.md`
- Empirical private WQ run and full-universe Lingxi FunctionEvolve-memory promotion audit are still future experiments, not yet committed evidence.
- Sanitized WQ template validation command: `python scripts\validate_sanitized_wq_run.py ara_artifacts\wq_alpha_evolution\evidence\templates\sanitized_wq_run_template.csv --allow-empty`

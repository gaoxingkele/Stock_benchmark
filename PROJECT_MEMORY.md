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
- `ara_artifacts/case_lingxi/PAPER.md`
- `paper/outline.md`
- `paper/abstract.md`
- `paper/introduction.md`
- `paper/method.md`
- `paper/experiments.md`

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

## Reproduction Commands

```powershell
python scripts\run_lingxi_pitnorm_tuned_gate_validation.py --test-end 2026-06-18 --out-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd
python scripts\run_lingxi_adaptive_router_validation.py --source-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd --out-dir experiments\lingxi_adaptive_router_validation_2026_ytd
python scripts\run_lingxi_regime_router_validation.py --out-dir experiments\lingxi_regime_router_validation_2026_ytd
python scripts\run_lingxi_sparse_regime_router_validation.py --out-dir experiments\lingxi_sparse_regime_router_validation_2026_ytd
python scripts\run_lingxi_meta_selector_validation.py --out-dir experiments\lingxi_meta_selector_validation
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

## Active Next Goal: CASE-Lingxi

The current expanded objective is to execute the CASE-Lingxi research plan:

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

CASE-Lingxi paper draft:

- Draft path: `paper/`
- Current files: `outline.md`, `abstract.md`, `introduction.md`, `method.md`, `experiments.md`, `related_work.md`, `formulation.md`, `citation_map.md`.
- The draft intentionally frames routers, RL, and LLM tags as negative or research-only evidence unless they beat the static menu OOS.
- Core BibTeX entries are in `papers/metadata/references.bib`; full 31-method citation pass is still pending.
- 31-method citation coverage is tracked in `papers/metadata/case_lingxi_citation_coverage.csv`.
- Citation coverage validation command: `python scripts\validate_case_lingxi_citations.py`; current result is PASS with 4 added and 27 pending finance-registry entries.
- Draft BibTeX generation command: `python scripts\build_case_lingxi_draft_bib.py`; current result is 10 draft entries and 17 missing registry metadata rows.

CASE-Lingxi Level 2 ARA review:

- Report path: `ara_artifacts/case_lingxi/level2_report.json`
- Overall grade: Weak Accept
- Promotion audit now exists: `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv`
- Cost sensitivity now exists: `experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_summary.csv`
- Main remaining improvements: Sharpe/MDD bootstrap tests, complete 31-method BibTeX, nonlinear capacity/slippage stress tests.

# CASE-Lingxi Execution Plan

Date: 2026-06-23

This is the actionable work plan for turning the current Lingxi benchmark into a reproducible research artifact and paper.

## Phase 1: Baseline Lock

Status: completed.

Deliverables:

1. `docs/reports/benchmark_master_table.md`
2. `data/ara_method_registry.csv`
3. result checks for the existing experiment summaries

Acceptance criteria:

1. 31 finance methods have ARA and experiment-validation status.
2. Current Lingxi/PITNorm/Lingxi5/Lingxi10 evidence is indexed.
3. Rejected dynamic routers and meta-selector failures are recorded.

## Phase 2: Literature And Theory Lock

Status: completed.

Deliverables:

1. `docs/literature/agent_rl_strategy_evolution_survey.md`
2. `docs/theory/case_lingxi_framework.md`
3. BibTeX updates in `papers/metadata/references.bib`

Acceptance criteria:

1. Agent RL works are mapped to CASE modules.
2. LLMs are scoped as research/context agents, not direct traders.
3. The validation echo trap is defined as a paper-level contribution.
4. `papers/metadata/references.bib` has 46 validated entries and 31/31 finance-registry coverage.

## Phase 3: Conservative Router Experiment

Status: completed first pass.

Implementation target:

`scripts/run_case_lingxi_context_router.py`

Candidate sleeves:

1. Lingxi;
2. Lingxi-PITNorm;
3. ReturnFloor-gated Lingxi;
4. cash/light-risk state if the existing backtest protocol supports it.

State features:

1. rolling market return;
2. rolling volatility;
3. cross-sectional dispersion;
4. rolling drawdown;
5. turnover pressure;
6. breadth.

Acceptance criteria:

1. frozen lagged context inputs;
2. 2026 YTD OOS output;
3. comparison against fixed/static scenario menu;
4. no production promotion because it wins annualized return only 3/16, Sharpe only 3/16, and MDD 9/16.

Result report:

`docs/reports/case_lingxi_context_router_validation.md`

## Phase 4: Research-Only RL Router

Status: completed first pass.

Implementation target:

`scripts/run_case_lingxi_rl_router_baseline.py`

Design:

1. small discrete action set over approved sleeves;
2. reward = cost-adjusted return - drawdown penalty - turnover penalty;
3. no direct stock selection by RL;
4. frozen policy before OOS evaluation.

Acceptance criteria:

1. frozen 2023-2024 training period;
2. 2025-2026 YTD OOS output;
3. labeled research-only because it wins annualized return only 4/16, Sharpe only 4/16, and MDD only 6/16 versus the static menu.

Result report:

`docs/reports/case_lingxi_rl_router_validation.md`

## Phase 5: LLM Market-Tag Ablation

Status: completed first pass.

Implementation target:

`scripts/run_case_lingxi_llm_tag_ablation.py`

Rules:

1. LLM outputs structured tags only.
2. Tags are frozen by date before evaluation.
3. Tags cannot contain direct trades, weights, or future-event descriptions.
4. The ablation must compare with and without tags.

Acceptance criteria:

1. point-in-time tag files generated under `experiments/case_lingxi_llm_tag_ablation_2026_ytd/`;
2. tag schema `case_lingxi_market_tags_v1`;
3. 2026 YTD comparison against static menu and conservative context router;
4. labeled research-only because it wins annualized return 0/16, Sharpe 2/16, and MDD 7/16 versus the static menu.

Result report:

`docs/reports/case_lingxi_llm_tag_ablation.md`

## Phase 6: Paper Draft

Status: completed draft.

Deliverables:

1. `paper/outline.md`
2. `paper/abstract.md`
3. `paper/introduction.md`
4. `paper/method.md`
5. `paper/experiments.md`

Acceptance criteria:

1. every numeric claim links to a result artifact;
2. every method claim links to registry or literature notes;
3. failed routes are included as negative evidence;
4. production claims are narrower than research claims.
5. paper citations resolve against `papers/metadata/references.bib`.

## Phase 7: ARA Upgrade

Status: completed Level 1 and refreshed Level 2.

Target:

`ara_artifacts/case_lingxi/`

Expected structure:

```text
PAPER.md
logic/
  problem.md
  claims.md
  concepts.md
  experiments.md
  related_work.md
  solution/
    method.md
    constraints.md
src/
  environment.md
trace/
  exploration_tree.yaml
evidence/
  README.md
```

Acceptance criteria:

1. Level 1 ARA validation passes.
2. Claims point to experiment IDs.
3. Experiments point to exact CSVs/scripts.
4. Failed routers and meta-selectors are represented in the trace.

Current result:

```text
python C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py ara_artifacts/case_lingxi
ARA Level 1 structural check: PASS
```

Current Level 2 result:

```text
ara_artifacts/case_lingxi/level2_report.json
overall_grade=Accept
mean_score=4.0
```

## Phase 8: Statistical And Trading-Realism Audits

Status: completed first pass.

Deliverables:

1. `docs/reports/case_lingxi_promotion_audit.md`
2. `docs/reports/case_lingxi_cost_sensitivity.md`
3. `docs/reports/case_lingxi_capacity_slippage.md`

Acceptance criteria:

1. annualized-return, Sharpe, and MDD paired bootstrap intervals are computed for adaptive candidates;
2. linear cost sensitivity covers 0, 5, 10, 20, and 50 bps;
3. nonlinear capacity/slippage stress covers 0.5-10x AUM and 0-20 impact bps;
4. no adaptive candidate is promoted unless it passes the numeric promotion gate.

Current result:

1. no adaptive candidate has a positive lower-bound bootstrap CI win for annualized return, Sharpe, or MDD;
2. no adaptive candidate passes the production gate under linear cost sensitivity;
3. no adaptive candidate passes the production gate under nonlinear capacity/slippage stress.

## Phase 9: Bundle Validation

Status: completed.

Validation command:

```powershell
python scripts\validate_case_lingxi_bundle.py
```

The bundle validator checks:

1. expected row counts for CASE-Lingxi summary/detail CSV files;
2. 31/31 citation coverage;
3. BibTeX hygiene;
4. ARA Level 1 structure.

## Remaining Future Work

These are not blockers for the current CASE-Lingxi bundle:

1. choose a target venue/template and polish manuscript structure accordingly;
2. optionally add trace provenance timestamps for full research-process reconstruction;
3. optionally run a future frozen timestamped LLM-debate tag experiment;
4. optionally calibrate capacity with real ADV/liquidity data if live-trading readiness becomes a claim.

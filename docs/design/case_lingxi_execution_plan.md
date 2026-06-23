# CASE-Lingxi Execution Plan

Date: 2026-06-23

This is the actionable work plan for turning the current Lingxi benchmark into a reproducible research artifact and paper.

## Phase 1: Baseline Lock

Status: in progress.

Deliverables:

1. `docs/reports/benchmark_master_table.md`
2. `data/ara_method_registry.csv`
3. result checks for the existing experiment summaries

Acceptance criteria:

1. 31 finance methods have ARA and experiment-validation status.
2. Current Lingxi/PITNorm/Lingxi5/Lingxi10 evidence is indexed.
3. Rejected dynamic routers and meta-selector failures are recorded.

## Phase 2: Literature And Theory Lock

Status: in progress.

Deliverables:

1. `docs/literature/agent_rl_strategy_evolution_survey.md`
2. `docs/theory/case_lingxi_framework.md`
3. BibTeX updates in `papers/metadata/references.bib`

Acceptance criteria:

1. Agent RL works are mapped to CASE modules.
2. LLMs are scoped as research/context agents, not direct traders.
3. The validation echo trap is defined as a paper-level contribution.

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

Status: planned.

Implementation target:

`scripts/run_case_lingxi_rl_router_baseline.py`

Design:

1. small discrete action set over approved sleeves;
2. reward = cost-adjusted return - drawdown penalty - turnover penalty;
3. no direct stock selection by RL;
4. frozen policy before OOS evaluation.

Acceptance criteria:

1. must report both validation and OOS performance;
2. must report validation-to-OOS decay;
3. must be labeled research-only unless it beats the conservative fixed/static menu across multiple markets.

## Phase 5: LLM Market-Tag Ablation

Status: planned.

Implementation target:

`docs/data/llm_market_tags/` or equivalent timestamped evidence directory, plus a runner script if tags become machine-readable.

Rules:

1. LLM outputs structured tags only.
2. Tags are frozen by date before evaluation.
3. Tags cannot contain direct trades, weights, or future-event descriptions.
4. The ablation must compare with and without tags.

Acceptance criteria:

1. point-in-time tag file;
2. tag schema;
3. OOS comparison;
4. audit notes for leakage risk.

## Phase 6: Paper Draft

Status: planned.

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

## Phase 7: ARA Upgrade

Status: planned.

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

## Current Next Command Targets

```powershell
python scripts\run_lingxi_sota_upgrade_validation.py --out-dir experiments\lingxi_sota_upgrade_validation
python scripts\run_lingxi_pitnorm_tuned_gate_validation.py --test-end 2026-06-18 --out-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd
python scripts\run_lingxi_meta_selector_validation.py --out-dir experiments\lingxi_meta_selector_validation
```

New scripts to implement next:

```text
scripts/run_case_lingxi_rl_router_baseline.py
scripts/run_case_lingxi_llm_tag_ablation.py
```

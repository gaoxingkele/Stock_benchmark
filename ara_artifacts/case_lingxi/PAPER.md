---
title: "When Not to Adapt: Conservative Agentic Strategy Evolution for Non-stationary Financial Markets"
authors:
  - "Stock_benchmark research log"
year: 2026
venue: "working paper / ARA package"
ara_version: "1.0"
domain: "agentic quantitative strategy evolution"
keywords:
  - "Lingxi"
  - "agentic strategy evolution"
  - "non-stationary financial markets"
  - "strategy routing"
  - "out-of-sample validation"
claims_summary:
  - "Lingxi Adaptive Suite is currently supported as a conservative scenario-specific production menu."
  - "Conservative context routing, frozen RL routing, and structured market tags are research-only under current evidence."
  - "Validation-only strategy selection and universal dynamic routing are not supported as production replacements."
abstract: "CASE-Lingxi studies conservative agentic strategy evolution for non-stationary financial markets. The artifact separates alpha generation, strategy-layer routing, and research-layer agent evolution. Across A-share, US, HK, and crypto benchmarks, current evidence supports a scenario-specific Lingxi production menu, while dynamic routers, frozen RL routing, and structured market tags remain research-only because they do not consistently beat the static menu out of sample."
---

# CASE-Lingxi

CASE-Lingxi means **Conservative Agentic Strategy Evolution for Lingxi**.

The central thesis is:

> Agents should improve the research loop, not directly route trades, unless frozen out-of-sample evidence proves that the router beats the conservative static menu.

## Layer Index

### Cognitive Layer (`logic/`)

| File | Description |
|---|---|
| [problem.md](logic/problem.md) | Research problem and non-stationarity motivation |
| [claims.md](logic/claims.md) | Falsifiable claims and evidence bindings |
| [concepts.md](logic/concepts.md) | Key concepts and terminology |
| [experiments.md](logic/experiments.md) | Experiment IDs, scripts, metrics, and outcomes |
| [related_work.md](logic/related_work.md) | Finance, time-series, and agentic RL references |
| [solution/method.md](logic/solution/method.md) | CASE-Lingxi method summary |
| [solution/constraints.md](logic/solution/constraints.md) | Scope limits and known weaknesses |

### Physical Layer (`src/`)

| File | Description |
|---|---|
| [environment.md](src/environment.md) | Local scripts, data, reports, and result artifacts |

### Exploration Graph (`trace/`)

| File | Description |
|---|---|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG including dead ends and rejected routes |

### Evidence (`evidence/`)

| File | Description |
|---|---|
| [README.md](evidence/README.md) | Evidence index and claim bindings |
| [runs/case_lingxi_validations.md](evidence/runs/case_lingxi_validations.md) | Summary of local validation runs |

### Review

| File | Description |
|---|---|
| [level2_report.json](level2_report.json) | ARA Level 2 semantic rigor review |

## Current Status

Supported production state:

1. Use **Lingxi Adaptive Suite** as a conservative scenario-specific production menu.
2. Keep dynamic routers, RL routers, and structured market tags as research-only unless they beat the OOS promotion gate.
3. Preserve failed routes as negative evidence for the paper thesis.

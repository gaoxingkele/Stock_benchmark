---
title: "Agentic Alpha Evolution: A Reproducible ARA Protocol for Self-Evolving Factor Discovery"
authors:
  - "Stock_benchmark research log"
year: 2026
venue: "working paper / ARA package"
ara_version: "1.0"
domain: "agentic alpha discovery"
keywords:
  - "WorldQuant BRAIN"
  - "factor mining"
  - "self-evolving agents"
  - "Agent-Native Research Artifact"
  - "Lingxi"
claims_summary:
  - "Self-evolving factor-mining skills should be evaluated as research-loop systems before being compared as trading strategies."
  - "WorldQuant BRAIN evidence must be stored as sanitized aggregate metrics, not raw account-linked alpha identifiers, expressions, or PnL."
  - "A fair comparison against CASE-Lingxi requires loop-efficiency, failure-memory, correlation-control, and out-of-sample proxy metrics."
abstract: "This ARA defines a reproducible comparison protocol for a WorldQuant-style self-evolving alpha research skill and the existing CASE-Lingxi strategy-evolution framework. It separates private platform evidence from public proxy evidence, specifies sanitized metrics for WorldQuant BRAIN runs, and defines how the self-evolution loop can be compared with Lingxi-style strategy routing without leaking private alpha records."
---

# Agentic Alpha Evolution

This artifact tracks an independent ARA project for comparing a WorldQuant-style self-evolving factor-mining skill with the existing CASE-Lingxi research program.

The central thesis is:

> The useful scientific object is not a single discovered alpha, but the agentic research loop that generates, tests, diagnoses, remembers, and redirects future alpha searches.

## Layer Index

### Cognitive Layer (`logic/`)

| File | Description |
|---|---|
| [problem.md](logic/problem.md) | Research problem and comparison scope |
| [claims.md](logic/claims.md) | Falsifiable claims and required evidence |
| [concepts.md](logic/concepts.md) | Key concepts and terminology |
| [experiments.md](logic/experiments.md) | Experiment plan, metrics, and acceptance gates |
| [related_work.md](logic/related_work.md) | Related repositories, alpha-mining systems, and CASE-Lingxi links |
| [solution/method.md](logic/solution/method.md) | ARA-WQ method and comparison design |
| [solution/constraints.md](logic/solution/constraints.md) | Platform, privacy, and reproducibility limits |

### Physical Layer (`src/`)

| File | Description |
|---|---|
| [environment.md](src/environment.md) | Required local tools, optional WQ credentials, and public proxy setup |

### Exploration Graph (`trace/`)

| File | Description |
|---|---|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG including rejected comparison shortcuts |

### Evidence (`evidence/`)

| File | Description |
|---|---|
| [README.md](evidence/README.md) | Evidence index and claim bindings |
| [schemas/sanitized_wq_run_schema.csv](evidence/schemas/sanitized_wq_run_schema.csv) | Required columns for private WQ run summaries |
| [schemas/proxy_factor_run_schema.csv](evidence/schemas/proxy_factor_run_schema.csv) | Required columns for public proxy factor-mining runs |
| [schemas/cross_framework_comparison_schema.csv](evidence/schemas/cross_framework_comparison_schema.csv) | Required columns for WQ-vs-Lingxi comparison summaries |
| [current_cross_framework_comparison.csv](evidence/current_cross_framework_comparison.csv) | Current layer-aware baseline comparison |

## Current Status

This artifact is a protocol-level ARA, not a completed WQ run:

1. WorldQuant BRAIN credentials, alpha IDs, raw expressions, and PnL series are intentionally excluded.
2. The public comparison can be run through proxy factor libraries and the existing CASE-Lingxi benchmark outputs.
3. A future private run can fill the sanitized schemas without changing the research claims.

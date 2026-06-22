---
title: "R&D-Agent-Quant: A Multi-Agent Framework for Data-Centric Factors and Model Joint Optimization"
authors:
  - "Not specified in provided sources"
year: 2025
venue: "preprint"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2025_rd_agent_quant_li.pdf"
ara_version: "1.0"
domain: "alpha_factor_mining_agent"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2025_rd_agent_quant_li is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "Financial markets pose fundamental challenges for asset return prediction due to their high dimensionality, non-stationarity, and persistent volatility. Despite advances in large language models and multi-agent systems, current quantita- tive research pipelines suffer from limited automation, weak interpretability, and fragmented coordination across key components such as factor mining and model innovation. In this paper, we propose R&D-Agent for Quantitative Finance, in short R&D-Agent(Q), the first data-centric multi-agent framework designed to automate the full-stack research and development of quantitative strategies via coordinated factor-model co-optimization. R&D-Agent(Q) decomposes the quant process into two iterative stages: aResearchstage that dynamically sets goal-aligned prompts, formulates hypotheses based on domain priors, and maps them to concrete tasks, and aDevelopmentstage that employs a code-generation agent, Co-STEER, to implement task-specific code, which is then e"
---

# R&D-Agent-Quant: A Multi-Agent Framework for Data-Centric Factors and Model Joint Optimization

## Overview

This ARA package was compiled from the current `Stock_benchmark` repository state. It binds paper metadata, available PDF/text evidence, local validation results, and known limitations into the standard ARA layers.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Why the paper is included and what validation gap it addresses |
| [claims.md](logic/claims.md) | Falsifiable claims and proof experiment IDs |
| [concepts.md](logic/concepts.md) | Key local benchmark and method concepts |
| [experiments.md](logic/experiments.md) | Validation and reproduction plans |
| [related_work.md](logic/related_work.md) | Source paper and local benchmark relationships |
| [solution/constraints.md](logic/solution/constraints.md) | Scope, assumptions, and missing evidence |
| [solution/method.md](logic/solution/method.md) | Method/proxy summary grounded in repository evidence |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Local runtime, data, and evidence sources | C01, C02, C03 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research and verification DAG reconstructed from local evidence |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Evidence index |
| [source/source_overview.md](evidence/source/source_overview.md) | Metadata, PDF, and source overview |
| [runs/local_validation.md](evidence/runs/local_validation.md) | Exact local validation rows |

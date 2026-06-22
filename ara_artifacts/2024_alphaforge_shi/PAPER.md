---
title: "AlphaForge: A Framework to Mine and Dynamically Combine Formulaic Alpha Factors"
authors:
  - "Not specified in provided sources"
year: 2024
venue: "preprint"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2024_alphaforge_shi.pdf"
ara_version: "1.0"
domain: "alpha_factor_mining"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2024_alphaforge_shi is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "The complexity of financial data, characterized by its vari- ability and low signal-to-noise ratio, necessitates advanced methods in quantitative investment that prioritize both per- formance and interpretability.Transitioning from early man- ual extraction to genetic programming, the most advanced approach in the alpha factor mining domain currently em- ploys reinforcement learning to mine a set of combination factors with fixed weights. However, the performance of re- sultant alpha factors exhibits inconsistency, and the inflexi- bility of fixed factor weights proves insufficient in adapting to the dynamic nature of financial markets. To address this issue, this paper proposes a two-stage formulaic alpha gen- erating framework AlphaForge, for alpha factor mining and factor combination. This framework employs a generative- predictive neural network to generate factors, leveraging the robust spatial exploration capabilities inherent in deep learn- ing while concurrently preserving dive"
---

# AlphaForge: A Framework to Mine and Dynamically Combine Formulaic Alpha Factors

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

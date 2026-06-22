---
title: "AlphaPROBE: Alpha Mining via Principled Retrieval and On-graph biased evolution"
authors:
  - "Not specified in provided sources"
year: 2026
venue: "preprint"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2026_alphaprobe_guo.pdf"
ara_version: "1.0"
domain: "alpha_factor_mining"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2026_alphaprobe_guo is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "--- page 1 --- AlphaPROBE: Alpha Mining via Principled Retrieval and On-graph Biased Evolution Taian Guo1 2 Haiyang Shen 3† Junyu Luo 1 Binqi Chen 1 2 Hongjun Ding 4 Jinsheng Huang 1 2 Luchen Liu 2 Yun Ma3✉ Ming Zhang 1✉ Abstract Extracting signals through alpha factor mining is a fundamental challenge in quantitative finance. Existing automated methods primarily follow two paradigms: Decoupled Factor Generation, which treats factor discovery as isolated events, and Iterative Factor Evolution, which focuses on local parent-child refinements. However, both paradigms lack a global structural view, often treating factor pools as unstructured collections or fragmented chains, which leads to redundant search and limited diversity. To address these limitations, we introduce AlphaPROBE (Alpha Mining viaPrincipledRetrieval andOn-graph BiasedEvolution), a framework that reframes al- pha mining as the strategic navigation of a Di- rected Acyclic Graph (DAG). By modeling fac- tors as nodes and ev"
---

# AlphaPROBE: Alpha Mining via Principled Retrieval and On-graph biased evolution

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

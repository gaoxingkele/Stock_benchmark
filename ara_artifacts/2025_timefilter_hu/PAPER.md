---
title: "TimeFilter: Patch-Specific Spatial-Temporal Graph Filtration for Time Series Forecasting"
authors:
  - "Not specified in provided sources"
year: 2025
venue: "ICML 2025"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2025_timefilter_hu.pdf"
ara_version: "1.0"
domain: "time_series_graph_filter"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2025_timefilter_hu is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "--- page 1 --- TimeFilter: Patch-Specific Spatial-Temporal Graph Filtration for Time Series Forecasting Yifan Hu 1 * Guibin Zhang 2 * Peiyuan Liu 1 * Disen Lan 3 Naiqi Li 1 Dawei Cheng 4 Tao Dai5 Shu-Tao Xia1 Shirui Pan 6 Abstract Time series forecasting methods generally fall into two main categories: Channel Independent (CI) and Channel Dependent (CD) strategies. While CI overlooks important covariate relation- ships, CD captures all dependencies without dis- tinction, introducing noise and reducing gener- alization. Recent advances in Channel Clus- tering (CC) aim to refine dependency model- ing by grouping channels with similar charac- teristics and applying tailored modeling tech- niques. However, coarse-grained clustering strug- gles to capture complex, time-varying interac- tions effectively. To address these challenges, we propose TimeFilter, a GNN-based framework for adaptive and fine-grained dependency mod- eling. After constructing the graph from the input sequence, TimeFilt"
---

# TimeFilter: Patch-Specific Spatial-Temporal Graph Filtration for Time Series Forecasting

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

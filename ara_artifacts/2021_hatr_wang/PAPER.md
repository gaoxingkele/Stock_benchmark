---
title: "Hierarchical Adaptive Temporal-Relational Modeling for Stock Trend Prediction"
authors:
  - "Not specified in provided sources"
year: 2021
venue: "IJCAI 2021"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2021_hatr_wang.pdf"
ara_version: "1.0"
domain: "stock_trend_temporal_relational"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2021_hatr_wang is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "Stock trend prediction is a challenging task due to the non-stationary dynamics and complex mar- ket dependencies. Existing methods usually regard each stock as isolated for prediction, or simply de- tect their correlations based on a ﬁxed predeﬁned graph structure. Genuinely, stock associations stem from diverse aspects, the underlying relation sig- nals should be implicit in comprehensive graphs. On the other hand, the RNN network is mainly used to model stock historical data, while is hard to capture ﬁne-granular volatility patterns implied in different time spans. In this paper, we propose a novel Hierarchical Adaptive Temporal-Relational Network (HATR) to characterize and predict stock evolutions. By stacking dilated causal convolutions and gating paths, short- and long-term transition features are gradually grasped from multi-scale lo- cal compositions of stock trading sequences. Par- ticularly, a dual attention mechanism with Hawkes process and target-speciﬁc query is proposed t"
---

# Hierarchical Adaptive Temporal-Relational Modeling for Stock Trend Prediction

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

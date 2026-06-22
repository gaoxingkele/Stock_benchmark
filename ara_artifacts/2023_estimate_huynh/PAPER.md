---
title: "Efficient Integration of Multi-Order Dynamics and Internal Dynamics in Stock Movement Prediction"
authors:
  - "Not specified in provided sources"
year: 2023
venue: "WSDM 2023"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2023_estimate_huynh.pdf"
ara_version: "1.0"
domain: "stock_movement_hypergraph"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2023_estimate_huynh is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "Advances in deep neural network (DNN) architectures have en- abled new prediction techniques for stock market data. Unlike other multivariate time-series data, stock markets show two unique characteristics: (i) multi-order dynamics, as stock prices are affected by strong non-pairwise correlations (e.g., within the same industry); and (ii) internal dynamics, as each individual stock shows some par- ticular behaviour. Recent DNN-based methods capture multi-order dynamics using hypergraphs, but rely on the Fourier basis in the convolution, which is both inefficient and ineffective. In addition, they largely ignore internal dynamics by adopting the same model for each stock, which implies a severe information loss. In this paper, we propose a framework for stock movement pre- diction to overcome the above issues. Specifically, the framework includes temporal generative filters that implement a memory- based mechanism onto an LSTM network in an attempt to learn individual patterns per stock"
---

# Efficient Integration of Multi-Order Dynamics and Internal Dynamics in Stock Movement Prediction

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

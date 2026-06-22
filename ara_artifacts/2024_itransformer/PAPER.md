---
title: "iTransformer: Inverted Transformers Are Effective for Time Series Forecasting"
authors: ["Not specified in provided sources"]
year: 2024
venue: "ICLR 2024 Spotlight"
doi: "https://arxiv.org/abs/2310.06625"
ara_version: "1.0"
domain: "cross-domain time-series methodology"
keywords: ["time-series", "variate-attention", "forecasting", "Lingxi-upgrade", "TopK-ranking", "ARA"]
claims_summary:
  - "iTransformer: Inverted Transformers Are Effective for Time Series Forecasting contributes a variate_attention method family relevant to time-series modeling."
  - "The method is a candidate source for Cross-sectional variate-attention ranking proxy."
abstract: "Methodology-focused ARA package for iTransformer: Inverted Transformers Are Effective for Time Series Forecasting. This package is compiled from the local SOTA survey metadata and source URL, and is intended to guide Lingxi10/Lingxi5 upgrade validation. It is not an official reproduction of the paper."
---

# iTransformer: Inverted Transformers Are Effective for Time Series Forecasting

## Overview

This ARA captures the paper as a methodology source for continuous Lingxi10/Lingxi5 upgrades. The local repository has not yet run the official implementation. The package therefore separates source-grounded metadata from proposed local validation work.

Primary Lingxi use: `Cross-sectional variate-attention ranking proxy`.

Datasets registered for comparison: ETTh1, ETTh2, ETTm1, ETTm2, Weather, Electricity, Traffic, Exchange Rate, ILI.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Methodology gap and Lingxi relevance |
| [claims.md](logic/claims.md) | Falsifiable local-transfer claims |
| [concepts.md](logic/concepts.md) | Method concepts and boundaries |
| [experiments.md](logic/experiments.md) | Local validation plans |
| [related_work.md](logic/related_work.md) | Relationship to Lingxi and 31-paper ARA pool |
| [solution/constraints.md](logic/solution/constraints.md) | Transfer constraints and limitations |
| [solution/method.md](logic/solution/method.md) | Method summary and proposed proxy |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Local software/data assumptions | C01, C02 |

### Data Layer (`/data`)
| File | Description |
|------|-------------|
| [dataset.md](data/dataset.md) | Registered datasets mentioned in the survey metadata |
| [preprocessing.md](data/preprocessing.md) | Point-in-time preprocessing constraints |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Evidence index |
| [source/source_overview.md](evidence/source/source_overview.md) | Source and local metadata |
| [runs/local_validation.md](evidence/runs/local_validation.md) | Current validation status |

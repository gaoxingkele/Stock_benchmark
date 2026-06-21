---
title: "AdaRNN: Adaptive Learning and Forecasting of Time Series"
authors:
  - "Yuntao Du"
  - "Jindong Wang"
  - "Wenjie Feng"
  - "Sinno Pan"
  - "Tao Qin"
  - "Renjun Xu"
  - "Chongjun Wang"
year: 2021
venue: "venue_unverified"
doi: "https://arxiv.org/abs/2108.04443"
ara_version: "1.0"
domain: "time series forecasting / financial analysis"
keywords:
  - "expanded"
  - "domain adaptation"
  - "temporal covariate shift"
  - "Qlib"
claims_summary:
  - "AdaRNN: Adaptive Learning and Forecasting of Time Series is included as a candidate_expanded paper for time series forecasting / financial analysis."
  - "Independent local verification status is complete."
abstract: "Though time series forecasting has a wide range of real-world appli- cations, it is a very challenging task. This is because the statistical properties of a time series can vary with time, causing the distri- bution to change temporally, which is known as the distribution shift problem in the machine learning community. By far, it still remains unexplored to model time series from the distribution-shift perspective. In this paper, we formulate the Temporal Covariate Shift (TCS) problem for the time series forecasting. We propose Adaptive RNNs (AdaRNN) to tackle the TCS problem. AdaRNN is sequentially composed of two modules. The first module is referred to as Temporal Distribution Characterization, which aims to better characterize the distribution information in a time series. The sec- ond module is termed as Temporal Distribution Matching, which aims to reduce the distribution mismatch"
---
# AdaRNN: Adaptive Learning and Forecasting of Time Series

## Overview

This ARA was generated from the local downloaded paper corpus, extracted paper text, local
paper project materials, and experiment summary files in `Stock_benchmark`.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Motivation, gaps, and assumptions captured from registry/project context |
| [claims.md](logic/claims.md) | Falsifiable claims and verification status |
| [concepts.md](logic/concepts.md) | Key terms from the paper/project |
| [experiments.md](logic/experiments.md) | Local verification plans and run bindings |
| [related_work.md](logic/related_work.md) | Source repository and registry relationships |
| [solution/constraints.md](logic/solution/constraints.md) | Scope limits and missing evidence |
| [solution/method.md](logic/solution/method.md) | Method summary grounded in local notes |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Local data, code, and runtime sources | C02, C03 |
| [configs/](src/configs/) | Copied local reproduction configs when available | C03 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Source-bounded research and reproduction DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Evidence index and independent verification status |
| [source/source_overview.md](evidence/source/source_overview.md) | Registry, PDF, project, and text evidence |
| [runs/](evidence/runs/) | Local run summaries when available |

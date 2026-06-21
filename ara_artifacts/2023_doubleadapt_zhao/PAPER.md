---
title: "DoubleAdapt: A Meta-learning Approach to Incremental Learning for Stock Trend Forecasting"
authors:
  - "Lifan Zhao"
  - "Shuming Kong"
  - "Yanyan Shen"
year: 2023
venue: "KDD 2023"
doi: "https://arxiv.org/abs/2306.09862"
ara_version: "1.0"
domain: "incremental stock trend forecasting"
keywords:
  - "CCF-A"
  - "concept drift"
  - "meta-learning"
  - "incremental learning"
  - "Qlib"
claims_summary:
  - "DoubleAdapt: A Meta-learning Approach to Incremental Learning for Stock Trend Forecasting is included as a candidate_verified paper for incremental stock trend forecasting."
  - "Independent local verification status is complete."
abstract: "Stock trend forecasting is a fundamental task of quantitative invest- ment where precise predictions of price trends are indispensable. As an online service, stock data continuously arrive over time. It is practical and efficient to incrementally update the forecast model with the latest data which may reveal some new patterns recurring in the future stock market. However, incremental learning for stock trend forecasting still remains under-explored due to the challenge of distribution shifts (a.k.a. concept drifts). With the stock market dynamically evolving, the distribution of future data can slightly or significantly differ from incremental data, hindering the effective- ness of incremental updates. To address this challenge, we propose DoubleAdapt, an end-to-end framework with two adapters, which can effectively adapt the data and the model to mitigate the effects of distribution sh"
---
# DoubleAdapt: A Meta-learning Approach to Incremental Learning for Stock Trend Forecasting

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

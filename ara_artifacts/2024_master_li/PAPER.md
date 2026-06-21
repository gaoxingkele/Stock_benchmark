---
title: "MASTER: Market-Guided Stock Transformer for Stock Price Forecasting"
authors:
  - "Tong Li"
  - "Zhaoyang Liu"
  - "Yanyan Shen"
  - "Xue Wang"
  - "Haokun Chen"
  - "Sen Huang"
year: 2024
venue: "AAAI 2024"
doi: "https://arxiv.org/abs/2312.15235"
ara_version: "1.0"
domain: "stock price/ranking forecasting"
keywords:
  - "CCF-A"
  - "stock transformer"
  - "market-guided gating"
  - "cross-time stock correlation"
claims_summary:
  - "MASTER: Market-Guided Stock Transformer for Stock Price Forecasting is included as a candidate_verified paper for stock price/ranking forecasting."
  - "Independent local verification status is complete."
abstract: "Stock price forecasting has remained an extremely challeng- ing problem for many decades due to the high volatility of the stock market. Recent efforts have been devoted to modeling complex stock correlations toward joint stock price forecast- ing. Existing works share a common neural architecture that learns temporal patterns from individual stock series and then mixes up temporal representations to establish stock correla- tions. However, they only consider time-aligned stock cor- relations stemming from all the input stock features, which suffer from two limitations. First, stock correlations often oc- cur momentarily and in a cross-time manner. Second, the fea- ture effectiveness is dynamic with market variation, which af- fects both the stock sequential patterns and their correlations. To address the limitations, this paper introduces MASTER, a MArkert-Guided Stock TransformER, whic"
---
# MASTER: Market-Guided Stock Transformer for Stock Price Forecasting

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

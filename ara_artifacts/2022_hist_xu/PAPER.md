---
title: "HIST: A Graph-based Framework for Stock Trend Forecasting via Mining Concept-Oriented Shared Information"
authors:
  - "Wentao Xu"
  - "Weiqing Liu"
  - "Lewen Wang"
  - "Yingce Xia"
  - "Jiang Bian"
  - "Jian Yin"
  - "Tie-Yan Liu"
year: 2022
venue: "preprint/venue_unverified"
doi: "https://arxiv.org/abs/2110.13716"
ara_version: "1.0"
domain: "stock trend forecasting"
keywords:
  - "secondary"
  - "graph learning"
  - "concept-oriented shared information"
  - "Qlib"
claims_summary:
  - "HIST: A Graph-based Framework for Stock Trend Forecasting via Mining Concept-Oriented Shared Information is included as a candidate_secondary paper for stock trend forecasting."
  - "Independent local verification status is complete."
abstract: "Stock trend forecasting, which forecasts stock prices’ future trends, plays an essential role in investment. The stocks in a market can share information so that their stock prices are highly correlated. Several methods were recently proposed to mine the shared infor- mation through stock concepts (e.g., technology, Internet Retail) extracted from the Web to improve the forecasting results. However, previous work assumes the connections between stocks and con- cepts are stationary, and neglects the dynamic relevance between stocks and concepts, limiting the forecasting results. Moreover, ex- isting methods overlook the invaluable shared information carried by hidden concepts, which measure stocks’ commonness beyond the manually defined stock concepts. To overcome the shortcom- ings of previous work, we proposed a novel stock trend forecasting framework that can adequately mine the concep"
---
# HIST: A Graph-based Framework for Stock Trend Forecasting via Mining Concept-Oriented Shared Information

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

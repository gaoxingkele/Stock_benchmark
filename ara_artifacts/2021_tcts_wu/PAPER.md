---
title: "Temporally Correlated Task Scheduling for Sequence Learning"
authors:
  - "Xueqing Wu et al."
year: 2021
venue: "ICML 2021"
doi: "https://proceedings.mlr.press/v139/wu21e/wu21e.pdf"
ara_version: "1.0"
domain: "time series forecasting / alpha seeking"
keywords:
  - "expanded"
  - "CCF-A"
  - "multi-task"
  - "Qlib"
claims_summary:
  - "Temporally Correlated Task Scheduling for Sequence Learning is included as a candidate_expanded paper for time series forecasting / alpha seeking."
  - "Independent local verification status is complete."
abstract: "--- page 1 --- Temporally Correlated Task Scheduling for Sequence Learning Xueqing Wu 1 Lewen Wang 2 Yingce Xia 2 Weiqing Liu 2 Lijun Wu 2 Shufang Xie 2 Tao Qin 2 Tie-Yan Liu 2 Abstract Sequence learning has attracted much research attention from the machine learning community in recent years. In many applications, a sequence learning task is usually associated with multiple temporally correlated auxiliary tasks, which are different in terms of how much input information to use or which future step to predict. For exam- ple, (i) in simultaneous machine translation, one can conduct translation under different latency (i.e., how many input words to read/wait before translation); (ii) in stock trend forecasting, one can predict the price of a stock in different future days (e.g., tomorrow, the day after tomorrow). While it is clear that those temporally correlated tasks can help each other,"
---
# Temporally Correlated Task Scheduling for Sequence Learning

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

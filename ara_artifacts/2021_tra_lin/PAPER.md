---
title: "Learning Multiple Stock Trading Patterns with Temporal Routing Adaptor and Optimal Transport"
authors:
  - "Hengxu Lin"
  - "Dong Zhou"
  - "Weiqing Liu"
  - "Jiang Bian"
year: 2021
venue: "KDD 2021"
doi: "https://arxiv.org/abs/2106.12950"
ara_version: "1.0"
domain: "stock trend/ranking prediction"
keywords:
  - "CCF-A"
  - "stock prediction"
  - "mixture-of-experts"
  - "optimal transport"
  - "Qlib"
claims_summary:
  - "Learning Multiple Stock Trading Patterns with Temporal Routing Adaptor and Optimal Transport is included as a candidate_verified paper for stock trend/ranking prediction."
  - "Independent local verification status is complete."
abstract: "Successful quantitative investment usually relies on precise pre- dictions of the future movement of the stock price. Recently, ma- chine learning based solutions have shown their capacity to give more accurate stock prediction and become indispensable compo- nents in modern quantitative investment systems. However, the i.i.d. assumption behind existing methods is inconsistent with the existence of diverse trading patterns1 in the stock market, which inevitably limits their ability to achieve better stock prediction performance. In this paper, we propose a novel architecture, Tem- poral Routing Adaptor (TRA), to empower existing stock prediction models with the ability to model multiple stock trading patterns. Essentially, TRA is a lightweight module that consists of a set of independent predictors for learning multiple patterns as well as a router to dispatch samples to different predic"
---
# Learning Multiple Stock Trading Patterns with Temporal Routing Adaptor and Optimal Transport

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

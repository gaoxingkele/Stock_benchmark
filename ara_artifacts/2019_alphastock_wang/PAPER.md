---
title: "AlphaStock: A Buying-Winners-and-Selling-Losers Investment Strategy using Interpretable Deep Reinforcement Attention Networks"
authors:
  - "Not specified in provided sources"
year: 2019
venue: "KDD 2019"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2019_alphastock_wang.pdf"
ara_version: "1.0"
domain: "portfolio_reinforcement_learning"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2019_alphastock_wang is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "Recent years have witnessed the successful marriage of finance innovations and AI techniques in various finance applications in- cluding quantitative trading (QT). Despite great research efforts devoted to leveraging deep learning (DL) methods for building better QT strategies, existing studies still face serious challenges especially from the side of finance, such as the balance of risk and return, the resistance to extreme loss, and the interpretability of strategies, which limit the application of DL-based strategies in real- life financial markets. In this work, we propose AlphaStock, a novel reinforcement learning (RL) based investment strategy enhanced by interpretable deep attention networks, to address the above chal- lenges. Our main contributions are summarized as follows: i) We integrate deep attention networks with a Sharpe ratio-oriented re- inforcement learning framework to achieve a risk-return balanced investment strategy; ii) We suggest modeling interrelationships amon"
---

# AlphaStock: A Buying-Winners-and-Selling-Losers Investment Strategy using Interpretable Deep Reinforcement Attention Networks

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

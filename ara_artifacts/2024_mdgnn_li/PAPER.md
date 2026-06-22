---
title: "MDGNN: Multi-Relational Dynamic Graph Neural Network for Comprehensive and Dynamic Stock Investment Prediction"
authors:
  - "Not specified in provided sources"
year: 2024
venue: "AAAI 2024"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2024_mdgnn_li.pdf"
ara_version: "1.0"
domain: "stock_investment_graph"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2024_mdgnn_li is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "The stock market is a crucial component of the financial sys- tem, but predicting the movement of stock prices is challeng- ing due to the dynamic and intricate relations arising from various aspects such as economic indicators, financial reports, global news, and investor sentiment. Traditional sequential methods and graph-based models have been applied in stock movement prediction, but they have limitations in capturing the multifaceted and temporal influences in stock price move- ments. To address these challenges, the Multi-relational Dy- namic Graph Neural Network (MDGNN) framework is pro- posed, which utilizes a discrete dynamic graph to comprehen- sively capture multifaceted relations among stocks and their evolution over time. The representation generated from the graph offers a complete perspective on the interrelationships among stocks and associated entities. Additionally, the power of the Transformer structure is leveraged to encode the tem- poral evolution of multiplex rel"
---

# MDGNN: Multi-Relational Dynamic Graph Neural Network for Comprehensive and Dynamic Stock Investment Prediction

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

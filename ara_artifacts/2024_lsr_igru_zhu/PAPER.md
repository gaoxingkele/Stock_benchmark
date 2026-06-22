---
title: "LSR-IGRU: Stock Trend Prediction Based on Long Short-Term Relationships and Improved GRU"
authors:
  - "Not specified in provided sources"
year: 2024
venue: "CIKM 2024"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2024_lsr_igru_zhu.pdf"
ara_version: "1.0"
domain: "stock_trend_gru"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2024_lsr_igru_zhu is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "Stock price prediction is a challenging problem in the field of fi- nance and receives widespread attention. In recent years, with the rapid development of technologies such as deep learning and graph neural networks, more research methods have begun to focus on exploring the interrelationships between stocks. However, existing methods mostly focus on the short-term dynamic relationships of stocks and directly integrating relationship information with temporal information. They often overlook the complex nonlin- ear dynamic characteristics and potential higher-order interaction relationships among stocks in the stock market. Therefore, we pro- pose a stock price trend prediction model named LSR-IGRU in this paper, which is based on long short-term stock relationships and an improved GRU input. Firstly, we construct a long short-term relationship matrix between stocks, where secondary industry in- formation is employed for the first time to capture long-term rela- tionships of stocks, a"
---

# LSR-IGRU: Stock Trend Prediction Based on Long Short-Term Relationships and Improved GRU

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

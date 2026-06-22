---
title: "DoubleEnsemble: A New Ensemble Method Based on Sample Reweighting and Feature Selection for Financial Data Analysis"
authors:
  - "Not specified in provided sources"
year: 2020
venue: "ICDM 2020"
doi: "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2020_doubleensemble_zhang.pdf"
ara_version: "1.0"
domain: "financial_model_ensemble"
keywords:
  - quantitative finance
  - stock prediction
  - benchmark
  - ARA
claims_summary:
  - "2020_doubleensemble_zhang is represented as a complete local ARA package."
  - "Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`."
abstract: "--- page 1 --- DoubleEnsemble: A New Ensemble Method Based on Sample Reweighting and Feature Selection for Financial Data Analysis 1st Chuheng Zhang Tsinghua University Beijing, China zhangchuheng123@live.com 4th Yifei Jin Tsinghua University, X-Tech Co. Ltd. Beijing, China yfjin1990@gmail.com 1st Yuanqi Li E-hualu Beijing, China liyq@ehualu.com 5th Pingzhong Tang Tsinghua University Beijing, China kenshinping@gmail.com 3rd Xi Chen New York University New York, USA xc13@stern.nyu.edu 6th Jian Li Tsinghua University Beijing, China lijian83@mail.tsinghua.edu.cn Abstract—Modern machine learning models (such as deep neural networks and boosting decision tree models) have become increasingly popular in ﬁnancial market prediction, due to their superior capacity to extract complex non-linear patterns. However, since ﬁnancial datasets have very low signal-to-noise ratio and are non-stationary, complex models are often very prone to overﬁtting and suffer from instability issues. Moreover, as va"
---

# DoubleEnsemble: A New Ensemble Method Based on Sample Reweighting and Feature Selection for Financial Data Analysis

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

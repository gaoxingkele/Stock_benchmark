# Method and Engineering Notes

## Paper digest

--- page 1 --- Temporally Correlated Task Scheduling for Sequence Learning Xueqing Wu 1 Lewen Wang 2 Yingce Xia 2 Weiqing Liu 2 Lijun Wu 2 Shufang Xie 2 Tao Qin 2 Tie-Yan Liu 2 Abstract Sequence learning has attracted much research attention from the machine learning community in recent years. In many applications, a sequence learning task is usually associated with multiple temporally correlated auxiliary tasks, which are different in terms of how much input information to use or which future step to predict. For exam- ple, (i) in simultaneous machine translation, one can conduct translation under different latency (i.e., how many input words to read/wait before translation); (ii) in stock trend forecasting, one can predict the price of a stock in different future days (e.g., tomorrow, the day after tomorrow). While it is clear that those temporally correlated tasks can help each other, there is a very limited exploration on how to better leverage multiple auxiliary tasks to boost the performance of the main task. In this work, we introduce a learnable scheduler to sequence learning, which can adap- tively select auxiliary tasks for training depending on the model status and the current training data. The scheduler and the model for the main task are jointly trained through bi-level optimization. Experiments show that our method signiﬁcantly improves the performance of simultaneous ma- chine translation and stock trend forecasting. 1. Introduction Sequence learning (Sutskever et al., 2014; Bahdanau et al., 2014) is an important problem in deep learning, which cov- ers many applications including machine translation (Wu et al., 2016; Vaswani et al., 2017), time series predic- tion (Qin et al., 2017a; Zhang et al., 2017a), weather fore- casting (Shi et al., 2015; Kim et al., 2017), etc. In real-world applications, a sequence learning task is often associated with multiple temporally correlated tasks: (1) In simulta- 1University of Science and Technology of China, Hef

## Local project notes

## README.md

```text
# 2021 TCTS Wu

## Paper

- Title: Temporally Correlated Task Scheduling for Sequence Learning
- Authors: Xueqing Wu et al.
- Year: 2021
- Venue: ICML 2021 according to Qlib model zoo
- Code: `external_repos/microsoft__qlib/examples/benchmarks/TCTS`

## Benchmark Role

Transformer-style CCF-A time-series baseline available in Qlib's alpha benchmark pool.

## Status

- PDF URL still needs source verification.
- Code repository cloned through `microsoft/qlib`.

```

## notes.md

```text
# TCTS Notes

## Source Verification

- Paper: Temporally Correlated Task Scheduling for Sequence Learning.
- Venue: ICML 2021, PMLR 139.
- PDF: `https://proceedings.mlr.press/v139/wu21e/wu21e.pdf`.
- Reproduction code referenced by Qlib: `https://github.com/lwwang1995/tcts`.
- Qlib baseline code: `external_repos/microsoft__qlib/examples/benchmarks/TCTS`.

## Core Idea

TCTS treats sequence forecasting as a multi-task problem where auxiliary tasks are temporally correlated with the main task. In stock forecasting, these tasks correspond to returns at different future horizons. A learnable scheduler selects which auxiliary task should guide training at each step, and the forecasting model plus scheduler are optimized through a bilevel training process.

## Qlib Setting

The local Qlib benchmark config uses:

```text
external_repos/microsoft__qlib/examples/benchmarks/TCTS/workflow_config_tcts_Alpha360.yaml
```

The Qlib config defines three labels:

```text
Ref($close, -2) / Ref($close, -1) - 1
Ref($close, -3) / Ref($close, -1) - 1
Ref($close, -4) / Ref($close, -1) - 1
```

For the China A-share benchmark, the first smoke config is recorded at:

```text
configs/china_a_share_smoke.json
```

## Reproduction Notes

- Start from the same CSI300 provider as LightGBM and TRA.
- Use TCTS after a vanilla Transformer baseline, because TCTS adds a scheduler on top of multi-horizon sequence learning.
- The current 7-trading-day smoke sample can validate config wiring but is too short for a meaningful multi-horizon TCTS run.

```

## repo_analysis.md

```text
# TCTS Repository Analysis

## Repository

`microsoft/qlib`

## Status

Cloned locally at:

```text
external_repos/microsoft__qlib
```

## Notes

- Qlib benchmark README reports TCTS Alpha360 results.
- The base model is noted as GRU in the Qlib benchmark README.


```

## reproduction_plan.md

```text
# TCTS Reproduction Plan

## Local Code Entrypoints

```text
external_repos/microsoft__qlib/examples/benchmarks/TCTS/
```

First config:

```text
examples/benchmarks/TCTS/workflow_config_tcts_Alpha360.yaml
```

## China A-Share Adaptation

1. Use as a strong Transformer-style baseline after LightGBM and Transformer.
2. Run on the same CSI300 Alpha360 feature set as TRA.
3. Keep paper URL/venue metadata verification as a source-collection task.

## Expected Outputs

- Shared alpha metrics.
- Comparison against vanilla Transformer, TRA, and MASTER.


```

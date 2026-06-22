# Method Summary

## Paper direction

- **Paper ID**: `2022_ddg_da_li`
- **Title**: DDG-DA: Data Distribution Generation for Predictable Concept Drift Adaptation
- **Task bucket**: stock_trend_concept_drift
- **Venue/status**: venue_unverified
- **Source group**: paper_24_matrix

## Local representation

This ARA represents the paper through local benchmark evidence rather than an invented official-code implementation.

Local comparison status: ready_for_metric_level_comparison.

## Abstract or digest

In many real-world scenarios, we often deal with streaming data that is sequentially collected over time. Due to the non- stationary nature of the environment, the streaming data dis- tribution may change in unpredictable ways, which is known as concept drift. To handle concept drift, previous methods ﬁrst detect when/where the concept drift happens and then adapt models to ﬁt the distribution of the latest data. How- ever, there are still many cases that some underlying factors of environment evolution are predictable, making it possible to model the future concept drift trend of the streaming data, while such cases are not fully explored in previous work. In this paper, we propose a novel method DDG-DA, that can effectively forecast the evolution of data distribution and im- prove the performance of models. Speciﬁcally, we ﬁrst train a predictor to estimate the future data distribution, then lever- age it to generate training samples, and ﬁnally train models on the generated data. We

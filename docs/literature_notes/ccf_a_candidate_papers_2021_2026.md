# CCF-A Candidate Papers: Stock Forecasting and Alpha Mining

Search date: 2026-06-18

Scope: recent five years, with priority on CCF-A conferences and direct relevance to stock/index trend forecasting or alpha factor mining.

## Core CCF-A Papers

| Paper ID | Paper | Venue | Main idea | Code | Benchmark priority |
| --- | --- | --- | --- | --- | --- |
| `2021_tra_lin` | Learning Multiple Stock Trading Patterns with Temporal Routing Adaptor and Optimal Transport | KDD 2021 | Add a Temporal Routing Adaptor with multiple predictors and optimal-transport-guided routing to capture multiple market regimes/patterns. | `microsoft/qlib/examples/benchmarks/TRA` | High |
| `2023_doubleadapt_zhao` | DoubleAdapt: A Meta-learning Approach to Incremental Learning for Stock Trend Forecasting | KDD 2023 | Two adapters for data adaptation and model adaptation under distribution shift/concept drift; meta-learning for incremental updates. | `SJTU-DMTai/qlib` | High |
| `2024_master_li` | MASTER: Market-Guided Stock Transformer for Stock Price Forecasting | AAAI 2024 | Market-guided feature gating plus alternating intra-stock/inter-stock/temporal attention for cross-time stock correlations. | `SJTU-DMTai/qlib` | High |

## Secondary Candidates

These are highly relevant but not currently in the verified CCF-A bucket.

| Paper ID | Paper | Venue/status | Main idea | Code | Use |
| --- | --- | --- | --- | --- | --- |
| `2022_hist_xu` | HIST: A Graph-based Framework for Stock Trend Forecasting via Mining Concept-Oriented Shared Information | Preprint / venue unverified | Graph framework for predefined and hidden stock concepts; relevant Qlib baseline. | `microsoft/qlib` | Baseline / ablation |
| `2022_thgnn_xiang` | Temporal and Heterogeneous Graph Neural Network for Financial Time Series Prediction | CIKM 2022 | Dynamic positive/negative correlation graph plus Transformer and heterogeneous GAT. | TBD | Related graph baseline |
| `2023_estimate_huynh` | Efficient Integration of Multi-Order Dynamics and Internal Dynamics in Stock Movement Prediction | WSDM 2023 | Temporal generative filters and wavelet hypergraph attention for stock movement prediction. | `thanhtrunghuynh93/estimate` | Related hypergraph baseline |
| `2024_alphaforge_shi` | AlphaForge: A Framework to Mine and Dynamically Combine Formulaic Alpha Factors | Preprint / venue unverified | Two-stage formulaic alpha generation and dynamic factor combination. | TBD | Alpha-mining candidate |
| `2026_alphaprobe_guo` | AlphaPROBE: Alpha Mining via Principled Retrieval and On-graph biased evolution | Preprint / venue unverified | DAG view of factor evolution, Bayesian factor retrieval, DAG-aware generation. | `gta0804/AlphaPROBE` | Alpha-mining candidate |

## Immediate Reproduction Direction

1. Start with `microsoft/qlib` as the shared benchmark substrate because it already contains data workflow, model zoo, backtest pipeline, and TRA.
2. Clone `SJTU-DMTai/qlib` separately because it contains DoubleAdapt and MASTER re-experiment code.
3. Standardize the first benchmark on a ranking label and IC/RankIC/backtest metrics, then add direction-classification metrics only for papers that require them.
4. Keep secondary candidates as baselines or later-stage modules after the CCF-A core is reproducible.


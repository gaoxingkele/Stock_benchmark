# Expanded CCF-A/B Candidate Scan

Search date: 2026-06-18

Expanded scope: CCF-A/B conferences and journals, plus strong open-source methods that are directly useful for stock/index forecasting or alpha factor mining.

## Verified Or Strong Mainline Candidates

| Paper ID | Method | Venue bucket | Task | Code | Notes |
| --- | --- | --- | --- | --- | --- |
| `2021_tra_lin` | TRA | CCF-A, KDD 2021 | Stock ranking / trend prediction | `microsoft/qlib/examples/benchmarks/TRA` | Core stock-specific model. |
| `2023_doubleadapt_zhao` | DoubleAdapt | CCF-A, KDD 2023 | Incremental stock trend forecasting | `SJTU-DMTai/qlib` | Core stock-specific concept-drift model. |
| `2024_master_li` | MASTER | CCF-A, AAAI 2024 | Stock price/ranking forecasting | `SJTU-DMTai/qlib` | Core stock-specific Transformer. |
| `2021_tcts_wu` | TCTS | CCF-A, ICML 2021 | Time-series forecasting / alpha seeking | `microsoft/qlib/examples/benchmarks/TCTS` | Qlib lists it as ICML 2021 and runnable in alpha benchmark. |

## Expanded Candidate Models

| Paper ID | Method | Venue/status | Task | Code | Reason to include |
| --- | --- | --- | --- | --- | --- |
| `2021_adarnn_du` | AdaRNN | Venue unverified in this pass | Time-series forecasting / financial analysis | `microsoft/qlib/examples/benchmarks/ADARNN` | Handles temporal covariate shift; Qlib benchmark includes it. |
| `2022_ddg_da_li` | DDG-DA | Venue unverified in this pass | Stock price trend / predictable concept drift | `microsoft/qlib` | Explicit stock trend experiment; complements DoubleAdapt. |
| `2022_hist_xu` | HIST | Venue unverified in this pass | Stock trend forecasting | `microsoft/qlib` | Stock-specific graph/concept model; important Qlib baseline. |
| `2022_thgnn_xiang` | THGNN | Reported CIKM 2022, needs final venue check | Financial time-series prediction | TBD | Dynamic heterogeneous graph baseline. |
| `2023_estimate_huynh` | ESTIMATE | Reported WSDM 2023, needs final venue check | Stock movement prediction | `thanhtrunghuynh93/estimate` | Hypergraph/wavelet attention baseline. |
| `2024_alphaforge_shi` | AlphaForge | Preprint / venue unverified | Formulaic alpha mining | TBD | Direct alpha-factor generation and dynamic combination. |
| `2026_alphaprobe_guo` | AlphaPROBE | Preprint / venue unverified | Alpha factor mining | `gta0804/AlphaPROBE` | Recent open-source DAG-guided alpha mining. |
| `2025_rd_agent_quant_li` | R&D-Agent-Quant | Preprint | Automated factor/model optimization | `microsoft/RD-Agent` | Practical high-star factor-mining automation direction. |

## Qlib Runnable Baseline Pool

Qlib's benchmark directory is useful because it already evaluates model scores as mined alpha through IC/RankIC and portfolio construction metrics. The directly runnable model pool includes:

| Group | Models |
| --- | --- |
| Tree/boosting baselines | LightGBM, XGBoost, CatBoost, DoubleEnsemble |
| Sequence baselines | LSTM, GRU, ALSTM, TCN, TFT |
| Transformer-style baselines | Transformer, Localformer, TCTS |
| Graph/concept baselines | GATs, HIST, IGMTF |
| Market-adaptation models | TRA, AdaRNN, ADD, DDG-DA-related workflows |
| Other neural baselines | MLP, TabNet, KRNN, Sandwich |

## Practical Inclusion Rule

Use three tiers:

1. `core_ccf_a`: TRA, DoubleAdapt, MASTER, TCTS.
2. `expanded_ccf_ab_or_stock_specific`: HIST, THGNN, ESTIMATE, AdaRNN, DDG-DA.
3. `alpha_mining_and_infra`: AlphaForge, AlphaPROBE, R&D-Agent-Quant, Alphalens, vectorbt.

This keeps the main benchmark academically clean while still letting the codebase grow toward alpha-factor research.


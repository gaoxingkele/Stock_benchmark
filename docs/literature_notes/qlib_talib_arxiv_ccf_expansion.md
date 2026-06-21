# Qlib / TA-Lib / Alpha Mining 论文扩展清单

Search date: 2026-06-21

本清单扩展已有 CCF-A/B 候选，重点覆盖三类方向：

1. Qlib 及其可运行 benchmark 生态。
2. TA-Lib / technical indicators / Alpha158 / Alpha101 类特征工程。
3. LLM/Agent 驱动的 alpha mining 与动态因子组合。

## 已验证主线

| Paper ID | Paper | Venue/status | 基础设施关系 | 纳入理由 |
|---|---|---|---|---|
| `2020_qlib_yang` | Qlib: An AI-oriented Quantitative Investment Platform | arXiv 2020 | Qlib | 项目基座；定义数据、模型、回测和 Alpha158 等流程。Source: arXiv PDF `2009.11189` / Qlib paper. |
| `2021_tra_lin` | Learning Multiple Stock Trading Patterns with Temporal Routing Adaptor and Optimal Transport | KDD 2021 | Qlib benchmark | Microsoft Research 页面说明代码和数据在 `microsoft/qlib/examples/benchmarks/TRA`。 |
| `2023_doubleadapt_zhao` | DoubleAdapt: A Meta-learning Approach to Incremental Learning for Stock Trend Forecasting | KDD 2023 | SJTU-DMTai / Qlib fork | 官方仓库标注 KDD'23；核心分布漂移与在线适配方法。 |
| `2024_master_li` | MASTER: Market-Guided Stock Transformer for Stock Price Forecasting | AAAI 2024 | SJTU-DMTai / Qlib-style data | AAAI paper 和 GitHub 均确认 MASTER 是市场引导 Stock Transformer。 |
| `2022_hist_xu` | HIST: A Graph-based Framework for Stock Trend Forecasting via Mining Concept-Oriented Shared Information | arXiv / code available | Qlib-compatible stock benchmark | 通过概念共享信息和隐藏概念建模股票关系；适合作为 graph/concept baseline。 |

## Alpha Mining / Agent 方向

| Paper ID | Paper | Venue/status | 与 Qlib/TA-Lib 的关系 | 纳入理由 |
|---|---|---|---|---|
| `2025_rd_agent_quant_li` | R&D-Agent-Quant: A Multi-Agent Framework for Data-Centric Factors and Model Joint Optimization | arXiv 2025 | 可接 Qlib 数据/回测；自动 factor+model R&D | 明确面向 quant factor-model co-optimization，代码为 `microsoft/RD-Agent`。 |
| `2025_alphaagent_tang` | AlphaAgent: LLM-Driven Alpha Mining with Regularized Exploration to Counteract Alpha Decay | KDD 2025 / arXiv | 使用 factor operators；可映射到 TA-Lib/Alpha101/Alpha158 搜索空间 | 直接解决 alpha decay；覆盖 CSI500 与 S&P500。 |
| `2024_alphaforge_shi` | AlphaForge: A Framework to Mine and Dynamically Combine Formulaic Alpha Factors | arXiv 2024; GitHub claims AAAI2025 official implementation | Qlib 数据保存工具；formulaic alpha mining | 动态组合 formulaic alpha，和当前 Regime-Gated 动态权重方向高度相关。 |
| `2026_alphaprobe_guo` | AlphaPROBE: Alpha Mining via Principled Retrieval and On-graph biased evolution | arXiv 2026 | factor DAG / alpha pool，可接 Qlib panel | 把 alpha pool 建成 DAG，适合做下一阶段因子搜索结构。 |
| `2025_cogalpha_liu` | Cognitive Alpha Mining via LLM-Driven Code-Based Evolution | arXiv 2025/2026 | code-based factor generation，可把 TA-Lib 算子作为 primitive | 多市场 alpha discovery，与跨市场验证方向一致。 |

## Benchmark / Feature Engineering 方向

| Paper ID | Paper | Venue/status | 与 Qlib/TA-Lib 的关系 | 纳入理由 |
|---|---|---|---|---|
| `2025_quantbench_wang` | QuantBench: Benchmarking AI Methods for Quantitative Investment | arXiv / OpenReview / FITEE 2026 | 包含 Alpha101、Alpha158、模型和全流程回测 | 适合作为项目标准化 benchmark 参考。 |
| `2025_fintsb` | FinTSB: A Comprehensive and Practical Benchmark for Financial Time Series | arXiv 2025 | 金融时序 benchmark | 可补足 Qlib 以外的金融时序评估维度。 |
| `2024_technical_indicator_impact` | Assessing the Impact of Technical Indicators on Machine Learning Models for High-Frequency Stock Price Prediction | arXiv 2024 | 技术指标 / TA-Lib-style features | 支持在 panel 中扩展 RSI/MACD/Bollinger/EMA 等指标组。 |
| `2025_tin` | Technical Indicator Networks: An Interpretable Neural Approach | arXiv 2025 | 技术指标神经结构 | 可作为 TA-Lib 指标可解释建模方向。 |

## 工程落地优先级

1. `qlib_feature_expansion`: 在 `download_yahoo_market_panel.py` 或新脚本中增加 TA-Lib-style 指标，不强依赖 `ta-lib` C 扩展，先实现 RSI/MACD/Bollinger/ATR/EMA。
2. `alpha_operator_pool`: 把 Alpha101/Alpha158/TA-Lib 算子作为统一 primitive，供 AlphaAgent/AlphaForge/AlphaPROBE/RD-Agent(Q) 风格搜索使用。
3. `cross_market_protocol`: 继续维护 A股、美股、港股、crypto 四市场统一 H5 TopK 协议。
4. `official_method_tiers`: Qlib 原生可跑方法优先，其次 paper-inspired proxy，再其次纯论文待复现。

## 已用来源

- Qlib arXiv paper: https://arxiv.org/pdf/2009.11189
- TRA Microsoft Research page: https://www.microsoft.com/en-us/research/publication/learning-multiple-stock-trading-patterns-with-temporal-routing-adaptor-and-optimal-transport/
- DoubleAdapt official GitHub / arXiv: https://github.com/SJTU-DMTai/DoubleAdapt and https://arxiv.org/pdf/2306.09862
- MASTER AAAI / GitHub: https://ojs.aaai.org/index.php/AAAI/article/view/27767 and https://github.com/SJTU-DMTai/MASTER
- HIST arXiv / GitHub: https://arxiv.org/pdf/2110.13716 and https://github.com/Wentao-Xu/HIST
- RD-Agent(Q): https://arxiv.org/abs/2505.15155
- AlphaAgent: https://arxiv.org/abs/2502.16789
- AlphaForge: https://arxiv.org/abs/2406.18394 and https://github.com/dulyhao/alphaforge
- AlphaPROBE: https://arxiv.org/abs/2602.11917 and https://github.com/gta0804/AlphaPROBE
- QuantBench: https://arxiv.org/html/2504.18600v1 and https://openreview.net/forum?id=y6wVRmPwDu
- TA-Lib: https://ta-lib.org/

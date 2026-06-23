# Introduction

Adaptation is one of the central promises of machine learning for financial markets. Market regimes change, cross-sectional structure drifts, and signal decay can be rapid. This makes static models and fixed rules appear insufficient. However, financial adaptation is also unusually vulnerable to overfitting: a strategy can adapt to a validation window, recent volatility pattern, or market narrative while losing robustness out of sample.

This paper studies that tension through the Lingxi strategy family. The project began as an empirical search for strong TopK long-only stock and crypto strategies. The current best validated form is not a single universal dynamic router, but a conservative scenario-specific menu called Lingxi Adaptive Suite. That result is important because it challenges a common intuition: more adaptive machinery does not automatically produce a better trading system.

We propose CASE-Lingxi, short for Conservative Agentic Strategy Evolution for Lingxi. CASE-Lingxi separates three layers. The alpha layer produces per-asset scores. The strategy layer chooses sleeves, TopK settings, normalization, and risk controls. The research-evolution layer uses agents to propose candidates, run experiments, generate structured context, and audit failure modes. Production promotion is controlled by a conservative out-of-sample gate.

The distinction between research evolution and production routing is the core design choice. Agents and LLMs can be valuable for hypothesis generation, experiment automation, literature synthesis, and leakage audits. But they should not be allowed to directly override production routing unless their outputs beat simple static baselines after being frozen and tested out of sample.

The current evidence supports this conservative stance. A context router improves drawdown in several scenarios but does not broadly improve return or Sharpe. A frozen tabular RL router is also not robust enough to replace the static menu. Structured market tags, designed as a leakage-safe interface for future multi-LLM debate systems, do not create a production edge in the first ablation. Finally, a validation-only Sharpe selector fails in out-of-sample evaluation, which we call the validation echo trap.

The contributions are:

1. We formulate strategy-layer routing as a separate problem from alpha prediction.
2. We introduce CASE-Lingxi, a conservative agentic strategy-evolution framework with explicit production, research, and rejection states.
3. We document negative evidence for universal dynamic routing, frozen RL routing, LLM-compatible market tags, and validation-only meta-selection.
4. We provide a cross-market benchmark across A-share, US, HK, and crypto settings.
5. We package the research as an Agent-Native Research Artifact so claims, code, results, and failed paths remain linked.


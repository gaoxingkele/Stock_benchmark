# CASE-Lingxi Framework

CASE-Lingxi means **Conservative Agentic Strategy Evolution for Lingxi**.

The framework turns the current Lingxi experiments into a research thesis:

> In non-stationary financial markets, the most useful role for agents is not direct trade routing. The useful role is conservative strategy evolution: generating and auditing candidate strategies, then promoting only those that survive frozen out-of-sample evidence.

## Problem Formulation

We separate three layers:

1. **Alpha layer**: produces per-asset scores.
2. **Strategy layer**: chooses TopK, normalization, risk controls, and sleeves.
3. **Research-evolution layer**: proposes new modules and decides whether evidence is strong enough for promotion.

Most prior work focuses on the alpha layer. Lingxi results show that the strategy layer is equally important: a strong score can be damaged by a poor router, and a conservative normalization module can improve risk without changing the underlying alpha source.

## Current Empirical Anchor

The current evidence supports these facts:

1. Lingxi10 and Lingxi5 are the main production anchors.
2. PITNorm is the only first-pass SOTA-inspired module with broad risk-control value.
3. MScale, Patch, LinearGuard, and VarAttn proxies do not replace Lingxi.
4. Validation-Sharpe meta-selection failed OOS.
5. Universal dynamic routing is not ready for production.
6. A scenario-specific strategy menu is stronger than a single global router.

Authoritative result index: `docs/reports/benchmark_master_table.md`.

## Architecture

```text
Candidate generator
  -> implementation and frozen config
  -> experiment runner
  -> evidence collector
  -> conservative promotion gate
  -> production / research sleeve / rejected
  -> ARA memory
```

## Modules

### Candidate Generator

Inputs:

1. current production menu;
2. rejected routes;
3. literature registry;
4. market failure cases;
5. ARA memory.

Outputs:

1. new strategy modules;
2. ablations;
3. feature proposals;
4. market-context tags;
5. risk-control rules.

Allowed candidate families:

1. Lingxi variants;
2. PITNorm gates;
3. ReturnFloor gates;
4. bounded context routers;
5. research-only RL routers;
6. agent-generated alpha or feature modules.

### Market Context Encoder

The context encoder can use:

1. lagged market return and volatility;
2. cross-sectional dispersion;
3. market breadth;
4. rolling drawdown;
5. turnover pressure;
6. liquidity;
7. structured LLM macro tags, if frozen and timestamped.

The encoder must not use future returns or post-hoc narrative labels.

### Conservative Promotion Gate

A candidate can be promoted only if it passes all required gates:

1. point-in-time safety;
2. transaction-cost inclusion;
3. fixed train/validation/test split;
4. 2025 OOS check where available;
5. 2026 YTD OOS check where available;
6. market or scenario breadth appropriate to its claim;
7. no severe drawdown or turnover degradation unless explicitly scoped as aggressive research.

Promotion labels:

| Label | Meaning |
|---|---|
| `production` | can be used as the default or scenario-specific proxy |
| `risk_control_candidate` | improves risk but may reduce return |
| `research_sleeve` | useful in a narrow scenario only |
| `rejected` | failed OOS, overfit, too costly, or too unstable |

### Validation Echo Trap Detector

The validation echo trap is the pattern where a method wins the validation period but fails once frozen and tested OOS.

Current evidence:

1. validation-only Sharpe selector wins 2/16 in 2025;
2. wins 0/16 in 2026 YTD;
3. wins 1/16 in combined 2025-2026 YTD.

This should become a named contribution in the paper because it explains why naive dynamic adaptation is dangerous in financial strategy routing.

## Agent Role Boundary

Agents may:

1. propose hypotheses;
2. write candidate modules;
3. design ablations;
4. summarize market context;
5. critique leakage and overfitting;
6. update ARA memory.

Agents may not:

1. directly emit production trade weights;
2. choose a production router from validation Sharpe alone;
3. rewrite evidence after seeing OOS outcomes;
4. promote a strategy without frozen evidence.

## Main Hypotheses

H1: A conservative scenario-specific strategy menu outperforms a universal dynamic router in OOS robustness.

H2: Agentic strategy evolution improves research throughput and failure detection, but only if production promotion is separated from agent proposal.

H3: Non-stationarity treatment on a strong existing alpha score is more reliable than adding generic SOTA feature proxies.

H4: Validation-selected strategy routing is unstable in non-stationary markets and should be treated as a measurable failure mode.

## Experimental Matrix

Markets:

1. China A-share CSI300;
2. US large cap;
3. HK large cap;
4. crypto major.

Portfolios:

1. Top10;
2. Top5;
3. raw;
4. industry/size neutral where meaningful;
5. equal-weight long-only;
6. daily rebalance;
7. single-side 10 bps cost.

Time:

1. train/pre-validation: 2018-2022 where available;
2. validation: 2023-2024;
3. OOS: 2025;
4. latest OOS: 2026 YTD.

Comparison groups:

1. Lingxi;
2. PITNorm;
3. ReturnFloor;
4. conservative context router;
5. research-only RL router;
6. LLM-tag ablation;
7. 31 finance ARA methods;
8. selected agentic alpha-mining references.

## Paper Framing

Candidate title:

**When Not to Adapt: Conservative Agentic Strategy Evolution for Non-stationary Financial Markets**

Core novelty:

1. strategy-layer routing is separated from alpha prediction;
2. agentic research generation is separated from production deployment;
3. failed routers and failed meta-selectors become evidence, not discarded experiments;
4. ARA memory makes the research path reproducible;
5. cross-market OOS validation tests robustness rather than only in-sample ranking.

## Immediate Execution Plan

1. Keep `docs/reports/benchmark_master_table.md` as the live result index.
2. Use `data/ara_method_registry.csv` as the canonical 31-method comparison registry.
3. Implement a conservative context router that only selects from approved sleeves.
4. Implement a research-only RL router with bounded action space.
5. Add an LLM market-tag ablation with frozen timestamped tags.
6. Update ARA evidence after each experiment, including rejected candidates.

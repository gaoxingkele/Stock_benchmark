# When Not to Adapt: Conservative Agentic Strategy Evolution for Non-stationary Financial Markets

## 1. Introduction

Main message:

Non-stationary financial markets make adaptation necessary, but naive adaptation is dangerous. CASE-Lingxi argues that agentic systems should evolve and audit strategies at the research layer, while production promotion remains controlled by frozen out-of-sample evidence.

Key claims:

1. Strategy-layer routing is distinct from alpha prediction.
2. Validation-selected adaptation can fail out of sample.
3. Conservative scenario-specific menus can outperform universal dynamic routers.
4. Agents and LLMs are useful as hypothesis, audit, and context tools, not direct production traders.

## 2. Related Work

Finance:

1. Qlib
2. DoubleAdapt
3. RD-Agent-Quant
4. AlphaAgent / CogAlpha / AlphaPROBE
5. FinTSB / QuantBench

Time-series:

1. DLinear
2. Non-stationary Transformer
3. PatchTST
4. iTransformer
5. TimeMixer and time-series foundation models

Agentic RL:

1. Agent Lightning
2. RAGEN
3. multi-agent debate and collaborative LLM RL

Local references:

```text
data/ara_method_registry.csv
docs/literature/agent_rl_strategy_evolution_survey.md
docs/reports/lingxi10_lingxi5_sota_upgrade_survey.md
```

Draft section:

```text
paper/related_work.md
```

## 3. Problem Formulation

Define:

1. asset universe and daily H5 return target;
2. sleeve-level daily return streams;
3. static production menu;
4. router policy;
5. conservative promotion gate.

The objective is not maximum validation Sharpe. The objective is robust OOS promotion under cost and drawdown constraints.

Draft section:

```text
paper/formulation.md
```

## 4. Method: CASE-Lingxi

Components:

1. Lingxi production menu;
2. candidate generator;
3. market context encoder;
4. conservative promotion gate;
5. validation echo trap detector;
6. ARA memory.

Agent role:

1. propose candidates;
2. write experiments;
3. audit leakage and overfit;
4. generate structured tags;
5. never bypass OOS promotion.

## 5. Experiments

Markets:

1. China A-share
2. US large cap
3. HK large cap
4. Crypto major

Portfolios:

1. H5
2. Top10 / Top5
3. raw / industry-size neutral
4. equal-weight long-only
5. daily rebalance
6. single-side 10 bps cost

Experiments:

1. Lingxi/PITNorm/SOTA proxy benchmark
2. Conservative context router
3. Frozen tabular RL router
4. Structured LLM-compatible market-tag ablation
5. Validation-only meta-selector rejection

## 6. Results

Primary evidence:

```text
docs/reports/benchmark_master_table.md
docs/reports/case_lingxi_context_router_validation.md
docs/reports/case_lingxi_rl_router_validation.md
docs/reports/case_lingxi_llm_tag_ablation.md
docs/reports/lingxi_meta_selector_validation.md
```

Expected table groups:

1. Production menu summary.
2. Router wins versus static menu.
3. RL router OOS wins.
4. Market-tag ablation wins.
5. Validation echo trap evidence.

## 7. Discussion

Main discussion points:

1. Why static menus can beat dynamic routers.
2. Why drawdown gains alone are insufficient for promotion.
3. Why LLM market narratives need frozen tag schemas.
4. How agentic research can still be valuable despite negative router results.

## 8. Limitations

1. Static universe bias in some global market panels.
2. Proxy implementations do not equal all official model reproductions.
3. LLM tags are deterministic proxies in the first pass.
4. RL baseline is intentionally small.
5. Transaction cost is simplified to single-side 10 bps.

## 9. Conclusion

CASE-Lingxi supports a conservative principle:

> In financial markets, the most reliable role for agents is to accelerate strategy evolution and failure detection, not to directly override production routing without out-of-sample proof.

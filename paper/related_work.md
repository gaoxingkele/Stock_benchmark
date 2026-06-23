# Related Work

## Quantitative Investment Benchmarks And Platforms

Qlib provides an AI-oriented quantitative investment platform and is the closest infrastructure reference for repeatable factor/model experiments [@yang2020qlib]. In this project it is represented by `2020_qlib_yang` in `data/ara_method_registry.csv`.

FinTSB and QuantBench are benchmark-oriented references for financial time-series and quantitative investment evaluation. They motivate CASE-Lingxi's emphasis on reproducible protocols, fixed costs, cross-market testing, and explicit result artifacts.

Local evidence:

```text
data/ara_method_registry.csv
docs/reports/ara_engineering_experiment_audit_31.md
docs/reports/benchmark_master_table.md
```

## Adaptive Financial Prediction

DoubleAdapt is the central prior for incremental stock trend forecasting under distribution shift [@zhao2023doubleadapt]. It motivates the need for adaptation, but CASE-Lingxi asks a different question: whether strategy-layer adaptation should be promoted after out-of-sample testing.

Other finance adaptation or routing references in the local 31-method registry include TRA, TCTS, MASTER, HIST, DoubleEnsemble, AlphaForge, AlphaPROBE, and RD-Agent-Quant.

CASE-Lingxi differs from these works by treating failed adaptation as first-class evidence. The negative results for validation-only selection, context routing, RL routing, and market tags are part of the argument rather than discarded experiments.

## Time-Series SOTA And Non-Stationarity

The Lingxi SOTA upgrade survey reviewed methods such as DLinear, Non-stationary Transformer, PatchTST [@nie2023patchtst], iTransformer [@liu2024itransformer], TimeMixer, FEDformer, and time-series foundation models.

The practical result was conservative. Lightweight proxies for MScale, Patch, LinearGuard, and VarAttn did not replace Lingxi. PITNorm was the only first-pass module with broad risk-control value. This supports the paper's theme: method novelty is not enough; promotion requires scenario-level OOS evidence.

Local evidence:

```text
docs/reports/lingxi10_lingxi5_sota_upgrade_survey.md
docs/reports/lingxi_sota_upgrade_validation.md
experiments/lingxi_sota_upgrade_validation/lingxi_sota_upgrade_validation_summary.csv
```

## Agentic Alpha Mining And Research Automation

RD-Agent-Quant [@li2025rdagentquant], AlphaAgent [@tang2025alphaagent], CogAlpha, and AlphaPROBE are the closest finance-specific agentic references. They motivate using agents to generate factors, code, retrieval paths, and alpha hypotheses.

CASE-Lingxi adopts the agentic research loop but narrows the deployment claim. Agents may propose candidates and audits, but they do not directly control production trades. This is a deliberate response to the observed instability of adaptive routers in the current benchmark.

## Reinforcement Learning For Agents

Recent agent RL systems such as Agent Lightning [@luo2025agentlightning] and RAGEN [@wang2025ragen] motivate training and diagnosing multi-step agent behavior. Their relevant idea for CASE-Lingxi is trajectory-level optimization:

```text
hypothesis -> implementation -> validation -> OOS test -> promotion/rejection
```

CASE-Lingxi applies this at the research process level. It does not claim that current RL routers are production-ready. The frozen tabular RL router is intentionally a small negative control: it wins annualized return and Sharpe in only 4/16 scenarios versus the static menu.

Local evidence:

```text
docs/literature/agent_rl_strategy_evolution_survey.md
docs/reports/case_lingxi_rl_router_validation.md
```

## LLM Market Context And Multi-Agent Debate

LLMs may be useful for summarizing macro context, identifying regime narratives, and auditing experiments. However, narrative plausibility is not tradable evidence.

The structured market-tag ablation establishes a safe interface:

1. tags are frozen by date;
2. tags are structured;
3. tags cannot emit trades or weights;
4. tags are evaluated against the static menu.

The first tag router wins annualized return in 0/16 scenarios and Sharpe in 2/16 scenarios versus the static menu. This supports using LLMs as audit/context tools, not production routers.

Local evidence:

```text
docs/reports/case_lingxi_llm_tag_ablation.md
experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv
```

## Positioning

CASE-Lingxi's novelty is not a new alpha model. Its contribution is a conservative framework for deciding when not to adapt:

1. separate alpha prediction from strategy routing;
2. separate agentic research from production deployment;
3. treat negative router results as evidence;
4. require OOS promotion gates before production use;
5. preserve claims, code, and failed paths in an ARA package.

## Citation Status

The current BibTeX file is:

```text
papers/metadata/references.bib
```

The first citation pass covers the core infrastructure, adaptation, time-series, and agentic references used directly in the CASE-Lingxi argument. The full 31-method citation coverage checklist is:

```text
papers/metadata/case_lingxi_citation_coverage.csv
```

The full registry still needs primary-source verification before manuscript submission.

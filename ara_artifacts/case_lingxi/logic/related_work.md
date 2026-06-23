# Related Work

## Finance And Quant Benchmark References

- Qlib (`2020_qlib_yang` in `data/ara_method_registry.csv`)
- DoubleAdapt (`2023_doubleadapt_zhao`)
- RD-Agent-Quant (`2025_rd_agent_quant_li`)
- AlphaAgent (`2025_alphaagent_tang`)
- CogAlpha (`2025_cogalpha_liu`)
- FinTSB (`2025_fintsb`)
- QuantBench (`2025_quantbench_wang`)

The current 31-method finance registry is:

```text
data/ara_method_registry.csv
```

## Time-Series Method References

The cross-domain SOTA survey and ARA expansion include:

- DLinear / LTSF-Linear
- Non-stationary Transformer
- PatchTST
- iTransformer
- TimeMixer
- FEDformer
- TTM and other time-series foundation models

Primary local report:

```text
docs/reports/lingxi10_lingxi5_sota_upgrade_survey.md
```

## Agentic RL And Agent Evolution

Primary local survey:

```text
docs/literature/agent_rl_strategy_evolution_survey.md
```

The CASE-Lingxi interpretation is conservative:

1. use agents to generate and audit research candidates;
2. use RL routers as research baselines;
3. require frozen OOS promotion before production;
4. do not let LLMs directly emit trades.


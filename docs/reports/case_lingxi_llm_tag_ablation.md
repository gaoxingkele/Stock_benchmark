# CASE-Lingxi Structured LLM-Tag Ablation

Date: 2026-06-23

This report validates the first LLM-compatible market-tag ablation:

```text
scripts/run_case_lingxi_llm_tag_ablation.py
```

The experiment does **not** let an LLM trade. It creates frozen, auditable market-context tags from lagged market data using the same schema a multi-LLM debate system could later emit.

## Why This Matters

The user hypothesis was that a dynamic router might use broader market context, possibly via multiple LLMs debating current market state.

This experiment tests the conservative version of that idea:

1. market context is converted into structured tags;
2. tags are frozen by date;
3. tags cannot contain trades, weights, or future information;
4. the router may only select among approved Lingxi-family sleeves.

## Protocol

Input:

```text
experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/
```

Output:

```text
experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv
```

Rows: 128

Generated tag files:

```text
experiments/case_lingxi_llm_tag_ablation_2026_ytd/<market>/market_tags_h5_top<k>_<variant>.csv
```

Markets:

1. China A-share
2. US large cap
3. HK large cap
4. Crypto major

Portfolios:

1. H5
2. Top10 and Top5
3. raw and industry/size neutral variants
4. equal-weight long-only
5. daily rebalance
6. single-side 10 bps cost inherited from the source sleeve files

## Tag Schema

Schema version:

```text
case_lingxi_market_tags_v1
```

Fields:

1. `trend_tag`: `up`, `down`, or `mixed`
2. `volatility_tag`: `high` or `normal`
3. `drawdown_tag`: `calm`, `watch`, or `stress`
4. `breadth_tag`: `weak` or `broad`
5. `dispersion_tag`: `high` or `normal`
6. `llm_style_summary`: `risk_off_stress`, `risk_on_trend`, `selective_alpha`, `defensive`, or `balanced`

The current source is deterministic lagged market context. This is intentional: it establishes a leakage-safe protocol before replacing the tag source with timestamped multi-LLM debate outputs.

## Result Versus Static Menu

Across 16 market/TopK/variant scenarios:

| Metric | Tag router wins | Interpretation |
|---|---:|---|
| Annualized return | 0 / 16 | No return edge |
| Sharpe | 2 / 16 | No broad risk-adjusted edge |
| MDD | 7 / 16 | Some drawdown control, but weaker than needed |

## Result Versus Conservative Context Router

| Metric | Tag router wins | Interpretation |
|---|---:|---|
| Annualized return | 3 / 16 | Usually weaker |
| Sharpe | 3 / 16 | Usually weaker |
| MDD | 5 / 16 | No clear risk-control improvement |

## Scenario Details

| Market | TopK | Variant | Tag ann. | Menu ann. | Context ann. | Tag Sharpe | Menu Sharpe | Context Sharpe | Tag MDD | Decision |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| China A-share | 10 | raw | 113.84% | 127.61% | 121.46% | 6.96 | 6.80 | 7.44 | -14.69% | reject as replacement |
| China A-share | 10 | neutral | 64.67% | 100.75% | 71.20% | 4.67 | 5.86 | 5.16 | -23.94% | reject |
| China A-share | 5 | raw | 128.55% | 161.96% | 131.05% | 6.77 | 6.96 | 6.83 | -16.45% | reject |
| China A-share | 5 | neutral | 97.62% | 130.65% | 97.80% | 5.61 | 6.17 | 5.59 | -20.57% | reject |
| US large cap | 10 | raw | 49.41% | 49.52% | 47.10% | 5.72 | 6.11 | 5.75 | -14.51% | reject |
| US large cap | 10 | neutral | 40.50% | 37.46% | 41.45% | 5.12 | 5.01 | 5.45 | -16.71% | narrow, not enough |
| US large cap | 5 | raw | 60.60% | 69.14% | 65.45% | 5.86 | 6.40 | 6.15 | -14.59% | drawdown only |
| US large cap | 5 | neutral | 48.84% | 55.68% | 49.84% | 5.19 | 5.58 | 5.28 | -15.92% | drawdown only |
| HK large cap | 10 | raw | 38.01% | 41.60% | 38.59% | 2.92 | 3.30 | 3.06 | -15.63% | reject |
| HK large cap | 10 | neutral | 26.10% | 28.01% | 26.67% | 2.20 | 2.43 | 2.26 | -22.04% | reject |
| HK large cap | 5 | raw | 42.76% | 45.98% | 47.40% | 2.99 | 3.47 | 3.42 | -19.05% | reject |
| HK large cap | 5 | neutral | 29.41% | 33.28% | 29.85% | 2.25 | 2.58 | 2.28 | -20.44% | reject |
| Crypto major | 10 | raw | 69.68% | 72.62% | 73.54% | 2.48 | 2.59 | 2.62 | -60.04% | reject |
| Crypto major | 10 | neutral | 37.82% | 47.70% | 36.47% | 1.43 | 1.75 | 1.38 | -59.97% | reject |
| Crypto major | 5 | raw | 117.60% | 128.98% | 118.57% | 3.22 | 3.45 | 3.24 | -60.38% | reject |
| Crypto major | 5 | neutral | 72.80% | 79.08% | 71.96% | 2.10 | 2.21 | 2.08 | -63.59% | reject |

## Conclusion

Structured market tags do not improve the production strategy in this first pass.

The result is important for the paper:

1. market narratives can be made point-in-time and auditable;
2. a tag schema is useful for future LLM debate experiments;
3. but market tags alone did not beat the static menu or conservative context router;
4. therefore, LLMs should remain research/context/audit agents until a frozen tag system beats the OOS gate.

This strengthens the CASE-Lingxi claim:

> Agentic context is not automatically tradable alpha. It must be promoted by evidence, not by plausibility.

## Reproduction

```powershell
python scripts\run_case_lingxi_llm_tag_ablation.py --out-dir experiments\case_lingxi_llm_tag_ablation_2026_ytd
```

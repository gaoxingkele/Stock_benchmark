# Method

## Overview

CASE-Lingxi is a conservative strategy-evolution framework. Its goal is not to maximize the apparent intelligence of the router. Its goal is to prevent unproven adaptation from replacing a robust static menu.

The framework has four components:

1. production sleeve menu;
2. candidate router layer;
3. agentic research layer;
4. conservative promotion gate.

## Production Sleeve Menu

The current production anchor is Lingxi Adaptive Suite. It is a scenario-specific menu:

| Market | Scenario | Production proxy |
|---|---|---|
| China A-share | raw Top10/Top5 | Lingxi |
| China A-share | neutral Top10/Top5 | Lingxi |
| US large cap | Top10/Top5 | fixed/static baselines depending scenario |
| HK large cap | Top10/Top5 | PITNorm |
| Crypto major | raw Top10/Top5 | ReturnFloor-Gate |
| Crypto major | neutral Top10/Top5 | Lingxi or PITNorm |

The menu is deliberately simple. Every adaptive candidate is compared against this menu before promotion.

## Candidate Router Layer

The tested routers operate at the sleeve level, not the individual-stock level. The approved action set is:

```text
lingxi
lingxi_pitnorm
lingxi_pitnorm_gate_return_floor
```

This design limits the blast radius of routing errors. A router can only choose among already validated sleeves.

## Conservative Context Router

The context router starts from the static menu and switches only when lagged market stress is detected. Stress features include:

1. rolling market return;
2. rolling volatility;
3. 60-day drawdown;
4. breadth;
5. cross-sectional dispersion;
6. turnover pressure.

The router is implemented in:

```text
scripts/run_case_lingxi_context_router.py
```

## Frozen Tabular RL Router

The RL router is a research-only baseline. It discretizes lagged market context into a small state and learns action values from 2023-2024. The policy is frozen before evaluating 2025-2026 YTD.

The action set is the same approved sleeve set. The reward is:

```text
net_return - turnover_penalty - switch_penalty
```

The router is implemented in:

```text
scripts/run_case_lingxi_rl_router_baseline.py
```

## Structured Market Tags

The market-tag ablation defines a schema that future LLM debate systems can emit:

```text
trend_tag
volatility_tag
drawdown_tag
breadth_tag
dispersion_tag
llm_style_summary
```

The current experiment uses deterministic lagged context to generate tags. This avoids leakage and establishes a reproducible interface before introducing live LLM outputs.

The ablation is implemented in:

```text
scripts/run_case_lingxi_llm_tag_ablation.py
```

## Conservative Promotion Gate

A candidate can be promoted only if it beats the static menu out of sample under transaction costs and without unacceptable drawdown or turnover degradation.

Promotion states:

| State | Meaning |
|---|---|
| production | default or scenario-specific strategy |
| risk-control candidate | improves risk but may sacrifice return |
| research sleeve | narrow scenario value only |
| rejected | failed OOS, overfit, too costly, or too unstable |

Current status:

1. context router: research-only drawdown sleeve;
2. RL router: research-only negative control;
3. market-tag router: research-only negative control;
4. validation-only selector: rejected.


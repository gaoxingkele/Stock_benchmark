# CASE-Lingxi Promotion Gate

Date: 2026-06-23

This document turns the CASE-Lingxi conservative promotion idea into explicit promotion rules.

## Candidate States

| State | Meaning |
|---|---|
| `production` | Can be used as the default or scenario-specific proxy |
| `risk_control_candidate` | Improves drawdown or volatility but does not broadly improve return/Sharpe |
| `research_sleeve` | Useful in a narrow market or TopK scenario |
| `negative_control` | Useful as comparison evidence, not as a candidate |
| `rejected` | Failed OOS, overfit, too costly, or methodologically unsafe |

## Required Evidence

A candidate must have:

1. frozen script or config;
2. committed summary CSV;
3. daily return files or reconstructable daily outputs;
4. comparison against the static production menu;
5. transaction cost included;
6. no direct lookahead features;
7. documented train/validation/test split where learning is involved.

## Production Gate

A candidate can become `production` only if all conditions hold:

1. annualized return wins at least 10/16 scenarios versus the static menu;
2. Sharpe wins at least 10/16 scenarios versus the static menu;
3. MDD is not worse in more than 4/16 scenarios;
4. no single major market group is consistently degraded;
5. average turnover does not rise by more than 25% unless net return and Sharpe both clearly improve;
6. the candidate passes paired block-bootstrap robustness checks for annualized daily-return difference, Sharpe difference, and MDD difference.

Current candidates do not pass this gate.

## Risk-Control Gate

A candidate can become `risk_control_candidate` if:

1. MDD improves in at least 8/16 scenarios;
2. Sharpe does not lose in more than 10/16 scenarios;
3. annualized return loss is explicitly accepted as a risk-control tradeoff;
4. the candidate is not used as the default production sleeve.

Current status:

| Candidate | Return wins | Sharpe wins | MDD wins | State |
|---|---:|---:|---:|---|
| CASE context router | 3/16 | 3/16 | 9/16 | `risk_control_candidate` / research sleeve |
| Frozen tabular RL router | 4/16 | 4/16 | 6/16 | `negative_control` |
| Structured market-tag router | 0/16 | 2/16 | 7/16 | `negative_control` |
| Validation-only meta-selector | 1/16 combined | 1/16 combined | not promoted | `rejected` |

Promotion audit update:

`experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv` recomputes candidate-vs-menu metrics from aligned daily files and adds block-bootstrap intervals for annualized daily-return difference, Sharpe difference, and MDD difference. It finds:

| Candidate | Return wins | Sharpe wins | MDD wins | Positive ann. CI wins | Positive Sharpe CI wins | Positive MDD CI wins | State |
|---|---:|---:|---:|---:|---:|---:|---|
| CASE context router | 3/16 | 4/16 | 9/16 | 0/16 | 0/16 | 0/16 | `risk_control_candidate` |
| Frozen tabular RL router | 4/16 | 4/16 | 6/16 | 0/16 | 0/16 | 0/16 | `negative_control` |
| Structured market-tag router | 1/16 | 3/16 | 7/16 | 0/16 | 0/16 | 0/16 | `negative_control` |

Cost sensitivity update:

`experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_summary.csv` recomputes candidate-vs-menu metrics at 0, 5, 10, 20, and 50 bps. No candidate reaches the production gate at any tested cost level.

Capacity/slippage update:

`experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_summary.csv` recomputes candidate-vs-menu metrics under a nonlinear stress model with 10 bps linear cost, 0.5-10x AUM multipliers, and 0-20 impact bps. No candidate reaches the production gate under any tested capacity/slippage setting.

## Research Sleeve Gate

A candidate can become `research_sleeve` if:

1. it wins a clearly defined market/TopK/variant scenario;
2. it has a plausible mechanism;
3. the claim is scoped to that scenario only;
4. it is not generalized to production.

Examples:

1. context router as A-share raw drawdown-control sleeve;
2. future timestamped LLM tags if they improve one market without leakage;
3. future RL variants if they improve a narrow OOS market segment.

## Rejection Gate

A candidate is `rejected` if:

1. it wins validation but fails OOS;
2. it uses future information;
3. it cannot be reproduced from committed artifacts;
4. it worsens return and Sharpe broadly;
5. it requires unverifiable narrative judgment for production.

## Remaining Statistical Gate Work

Implemented:

1. candidate-minus-menu annualized daily-return difference;
2. paired block-bootstrap confidence interval;
3. Sharpe difference bootstrap interval;
4. MDD difference bootstrap interval;
5. linear cost sensitivity;
6. nonlinear capacity/slippage stress.

Remaining optional upgrades:

1. paired sign tests for daily return differences;
2. turnover-difference confidence intervals;
3. calibrated market-specific capacity model if real ADV/liquidity data is added.

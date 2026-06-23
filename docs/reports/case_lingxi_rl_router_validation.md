# CASE-Lingxi Research-Only RL Router Validation

Date: 2026-06-23

This report validates the research-only RL-style router:

```text
scripts/run_case_lingxi_rl_router_baseline.py
```

The router is not a production candidate. It is a controlled baseline for the question:

> Can a small frozen RL-style policy route approved Lingxi sleeves better than the conservative static menu?

Current answer: no.

## Protocol

Training period:

```text
2023-01-03 to 2024-12-31
```

OOS test period:

```text
2025-01-01 to 2026-06-11
```

Input source:

```text
experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/
```

Output:

```text
experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv
```

Rows: 128

Markets:

1. China A-share
2. US large cap
3. HK large cap
4. Crypto major

Actions:

1. `lingxi`
2. `lingxi_pitnorm`
3. `lingxi_pitnorm_gate_return_floor`

The policy never selects individual stocks directly.

## Method

The baseline is a frozen tabular state-action router.

State:

1. 20-day trend sign;
2. high/low 20-day volatility;
3. 60-day drawdown stress;
4. weak/strong breadth;
5. high/low cross-sectional dispersion.

Action values are learned from full-information sleeve returns in 2023-2024. The learned table is frozen before 2025 OOS evaluation.

Reward:

```text
net_return - turnover_penalty - switch_penalty
```

This is intentionally simple. The goal is not to claim a new RL algorithm, but to create a disciplined comparison point for future agentic or RL routers.

## Result Versus Static Menu

Across 16 market/TopK/variant scenarios:

| Metric | RL wins | Interpretation |
|---|---:|---|
| Annualized return | 4 / 16 | Not a broad return upgrade |
| Sharpe | 4 / 16 | Not a broad risk-adjusted upgrade |
| MDD | 6 / 16 | Weaker drawdown control than the conservative context router |

## Scenario Details

| Market | TopK | Variant | RL ann. | Menu ann. | RL Sharpe | Menu Sharpe | RL MDD | Menu MDD | Decision |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| China A-share | 10 | raw | 176.27% | 283.34% | 12.11 | 15.88 | -10.47% | -9.44% | reject |
| China A-share | 10 | neutral | 163.48% | 208.56% | 11.73 | 13.31 | -7.39% | -8.80% | drawdown only |
| China A-share | 5 | raw | 261.32% | 323.58% | 13.19 | 14.58 | -10.97% | -11.57% | reject |
| China A-share | 5 | neutral | 266.27% | 298.55% | 13.21 | 14.33 | -9.97% | -13.29% | drawdown only |
| US large cap | 10 | raw | 52.70% | 53.26% | 5.90 | 5.84 | -13.79% | -11.60% | mixed, not enough |
| US large cap | 10 | neutral | 31.95% | 31.58% | 4.02 | 3.85 | -17.01% | -16.56% | narrow Sharpe win, not enough |
| US large cap | 5 | raw | 61.70% | 71.40% | 5.53 | 6.15 | -13.99% | -16.73% | drawdown only |
| US large cap | 5 | neutral | 44.89% | 65.75% | 4.32 | 5.71 | -17.17% | -16.72% | reject |
| HK large cap | 10 | raw | 47.47% | 39.06% | 4.86 | 4.71 | -14.94% | -10.37% | return/Sharpe win, drawdown cost |
| HK large cap | 10 | neutral | 39.28% | 40.31% | 4.12 | 4.62 | -14.74% | -14.92% | reject |
| HK large cap | 5 | raw | 48.04% | 42.94% | 3.97 | 4.39 | -18.09% | -11.85% | reject despite return win |
| HK large cap | 5 | neutral | 48.95% | 43.74% | 4.73 | 4.50 | -13.74% | -15.12% | narrow research sleeve |
| Crypto major | 10 | raw | -28.43% | -25.01% | -1.35 | -1.17 | -60.88% | -60.15% | reject |
| Crypto major | 10 | neutral | -29.88% | -29.46% | -1.38 | -1.36 | -60.22% | -58.83% | reject |
| Crypto major | 5 | raw | -23.91% | -23.39% | -1.13 | -1.10 | -60.48% | -58.91% | reject |
| Crypto major | 5 | neutral | -30.36% | -29.78% | -1.51 | -1.50 | -63.08% | -62.04% | reject |

## Conclusion

The frozen tabular RL router does not beat the conservative static menu.

This strengthens the CASE-Lingxi paper argument:

1. even a disciplined frozen RL router is not automatically better than a simple scenario menu;
2. direct adaptive routing remains fragile under market non-stationarity;
3. agents and RL should first optimize the research process and candidate generation, not production routing;
4. any stronger RL router must clear this baseline and the static menu OOS before being considered for production.

## Reproduction

```powershell
python scripts\run_case_lingxi_rl_router_baseline.py --out-dir experiments\case_lingxi_rl_router_validation_2025_2026_ytd
```

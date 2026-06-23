# CASE-Lingxi Capacity and Slippage Stress Audit

Date: 2026-06-23

This report tests whether nonlinear capacity/slippage assumptions change the CASE-Lingxi promotion decision.

## Script

```text
scripts/run_case_lingxi_capacity_slippage.py
```

## Outputs

```text
experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_summary.csv
experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_detail.csv
```

Rows:

| Artifact | Rows |
|---|---:|
| Summary | 60 |
| Detail | 960 |

## Method

The stress test reconstructs gross return from the daily files:

```text
gross_return = net_return + cost
```

Then it applies a nonlinear stress model:

```text
stressed_return = gross_return
  - turnover * linear_cost_bps / 10000
  - turnover^2 * impact_bps * sqrt(aum_multiplier) / 10000
```

Settings:

| Setting | Values |
|---|---|
| Linear cost | 10 bps |
| AUM multiplier | 0.5, 1, 2, 5, 10 |
| Nonlinear impact bps | 0, 5, 10, 20 |

This is a conservative stress model, not a calibrated real-market impact model. Its purpose is to test whether the adaptive candidates are only rejected under a benign linear-cost assumption.

## Summary

Across 60 candidate/stress combinations:

| Candidate | Stress combinations | Max ann. wins | Max Sharpe wins | Max MDD wins | State distribution |
|---|---:|---:|---:|---:|---|
| Conservative context router | 20 | 3/16 | 5/16 | 10/16 | 20 risk-control candidate |
| Frozen tabular RL router | 20 | 6/16 | 5/16 | 6/16 | 20 not promoted |
| Structured market-tag router | 20 | 2/16 | 3/16 | 8/16 | 20 not promoted |

Best return-side case:

| Candidate | AUM multiplier | Impact bps | Ann. wins | Sharpe wins | MDD wins | State |
|---|---:|---:|---:|---:|---:|---|
| Frozen tabular RL router | 10 | 20 | 6/16 | 5/16 | 6/16 | not promoted |

## Conclusion

Nonlinear capacity/slippage stress does not overturn the production decision.

1. No adaptive candidate reaches the production gate under any tested AUM/impact combination.
2. The context router remains a drawdown-oriented risk-control candidate, not a production replacement.
3. The RL router improves relative return wins under severe nonlinear impact, but still falls far below the production gate.
4. The market-tag router remains a negative control.

This strengthens the final CASE-Lingxi position:

> The static production menu remains the default even after nonlinear slippage and capacity stress; adaptive routers remain research or audit tools.

## Reproduction

```powershell
python scripts\run_case_lingxi_capacity_slippage.py --out-dir experiments\case_lingxi_capacity_slippage
```

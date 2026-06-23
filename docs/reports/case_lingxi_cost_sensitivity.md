# CASE-Lingxi Cost Sensitivity Audit

Date: 2026-06-23

This report tests whether CASE-Lingxi promotion decisions change when single-side transaction cost changes from the default 10 bps.

## Script

```text
scripts/run_case_lingxi_cost_sensitivity.py
```

## Outputs

```text
experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_summary.csv
experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_detail.csv
```

Rows:

| Artifact | Rows |
|---|---:|
| Summary | 15 |
| Detail | 240 |

## Method

The source daily files include:

```text
net_return
cost
turnover
```

The audit reconstructs gross return:

```text
gross_return = net_return + cost
```

Then it recomputes net return at each cost level:

```text
net_return(cost_bps) = gross_return - turnover * cost_bps / 10000
```

Cost levels:

```text
0, 5, 10, 20, 50 bps
```

Candidates:

1. conservative context router;
2. frozen tabular RL router;
3. structured market-tag router.

Comparator:

1. CASE static production menu.

## Summary

| Candidate | Cost bps | Ann. wins | Sharpe wins | MDD wins | State |
|---|---:|---:|---:|---:|---|
| Context router | 0 | 3/16 | 5/16 | 10/16 | risk-control candidate |
| Context router | 5 | 3/16 | 4/16 | 9/16 | risk-control candidate |
| Context router | 10 | 3/16 | 4/16 | 9/16 | risk-control candidate |
| Context router | 20 | 3/16 | 5/16 | 10/16 | risk-control candidate |
| Context router | 50 | 3/16 | 3/16 | 11/16 | risk-control candidate |
| Frozen RL router | 0 | 4/16 | 4/16 | 6/16 | not promoted |
| Frozen RL router | 5 | 4/16 | 4/16 | 6/16 | not promoted |
| Frozen RL router | 10 | 4/16 | 4/16 | 6/16 | not promoted |
| Frozen RL router | 20 | 4/16 | 4/16 | 6/16 | not promoted |
| Frozen RL router | 50 | 6/16 | 6/16 | 4/16 | not promoted |
| Market-tag router | 0 | 1/16 | 3/16 | 9/16 | not promoted |
| Market-tag router | 5 | 1/16 | 4/16 | 9/16 | not promoted |
| Market-tag router | 10 | 1/16 | 3/16 | 7/16 | not promoted |
| Market-tag router | 20 | 2/16 | 3/16 | 9/16 | not promoted |
| Market-tag router | 50 | 3/16 | 1/16 | 7/16 | not promoted |

## Conclusion

Cost sensitivity does not overturn the production decision.

1. No adaptive candidate reaches the production gate at any tested cost level.
2. The context router remains a risk-control candidate because its MDD wins are consistent across costs.
3. The RL router improves relative return/Sharpe wins at 50 bps, but MDD wins drop to 4/16, so it still fails the production gate.
4. The market-tag router remains a negative control.

This strengthens the current CASE-Lingxi conclusion:

> The static production menu remains the default; adaptation is not promoted by changing transaction-cost assumptions within 0-50 bps.

## Reproduction

```powershell
python scripts\run_case_lingxi_cost_sensitivity.py --out-dir experiments\case_lingxi_cost_sensitivity
```

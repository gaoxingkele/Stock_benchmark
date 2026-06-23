# CASE-Lingxi Promotion Audit

Date: 2026-06-23

This report implements the Level 2 rigor-review recommendation to add a unified candidate-vs-menu promotion table and paired daily-return bootstrap intervals for annualized daily-return difference, Sharpe difference, and MDD difference.

## Script

```text
scripts/run_case_lingxi_promotion_audit.py
```

## Outputs

```text
experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv
experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_detail.csv
```

Rows:

| Artifact | Rows |
|---|---:|
| Summary | 3 |
| Detail | 48 |

## Method

For each candidate and scenario, the audit:

1. reads candidate and static-menu daily `net_return`;
2. aligns daily dates;
3. computes annualized return difference, Sharpe difference, and MDD difference;
4. runs a paired block bootstrap on aligned daily return paths;
5. records whether the 95% bootstrap interval lower bound is strictly positive for annualized daily-return difference, Sharpe difference, and MDD difference.

Bootstrap settings:

| Setting | Value |
|---|---:|
| Samples | 1000 |
| Block size | 5 |
| Seed | 20260623 |

## Summary

| Candidate | Scenarios | Ann. wins | Sharpe wins | MDD wins | Positive ann. CI wins | Positive Sharpe CI wins | Positive MDD CI wins | State |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Conservative context router | 16 | 3 | 4 | 9 | 0 | 0 | 0 | risk-control candidate |
| Frozen tabular RL router | 16 | 4 | 4 | 6 | 0 | 0 | 0 | negative control |
| Structured market-tag router | 16 | 1 | 3 | 7 | 0 | 0 | 0 | negative control |

The audit slightly differs from earlier hand summaries because it recomputes annualized return and Sharpe from aligned daily files. The conclusion is unchanged and stricter: no candidate has a scenario where the annualized daily-return difference, Sharpe difference, or MDD difference bootstrap lower bound is positive.

## Promotion Decision

No candidate passes the production gate.

Production gate from `docs/theory/case_lingxi_promotion_gate.md`:

1. annualized return wins at least 10/16 scenarios;
2. Sharpe wins at least 10/16 scenarios;
3. MDD is not worse in more than 4/16 scenarios;
4. positive paired-return confidence evidence after the statistical audit.

Current decision:

| Candidate | Decision | Reason |
|---|---|---|
| Conservative context router | keep as risk-control research sleeve | MDD wins 9/16 but annualized return and Sharpe wins are too sparse; no positive annualized-diff CI wins |
| Frozen tabular RL router | negative control | too few wins and no positive annualized/Sharpe/MDD CI wins |
| Structured market-tag router | negative control | too few wins and no positive annualized/Sharpe/MDD CI wins |

## Interpretation

This audit strengthens the paper thesis:

> Adaptation is plausible and sometimes improves drawdown, but current adaptive candidates do not clear a conservative promotion gate against a simple static menu.

The result also strengthens the agentic framing. Agents, RL, and LLM tags remain useful for research generation and auditing, but current evidence does not justify letting them override production routing.

## Reproduction

```powershell
python scripts\run_case_lingxi_promotion_audit.py --out-dir experiments\case_lingxi_promotion_audit
```

# Custom A-share Basket Backtest 2025-2026

Date: 2026-06-24

## Universe

The user supplied 49 A-share tickers. Public data fetch covered 48 tickers. The only missing ticker was:

```text
920357.BJ
```

## Method

Backtest command:

```powershell
python scripts\run_custom_a_share_basket_backtest.py --start 20250101 --end 20260624 --cost-bps 10 --out-dir experiments\custom_a_share_basket_2025_2026 --sleep 0.02
```

Assumptions:

1. daily equal-weight long-only basket;
2. close-to-close returns;
3. daily rebalance to available constituents;
4. one-way cost 10 bps;
5. historical adjusted close from public AkShare sources with local fallback.

The Top5/Top10/Top20 baskets are the first 5/10/20 tickers in the user-provided order, not model-selected ranks.

## Results

Output:

```text
experiments/custom_a_share_basket_2025_2026/custom_a_share_basket_summary.csv
```

| Basket | Covered | Period | Ann Return | Sharpe | MDD | Cum Return |
|---|---:|---|---:|---:|---:|---:|
| Top5 | 5/5 | 2025-01-03 to 2026-06-24 | 1.54015858 | 4.79447662 | -0.19150913 | 2.70452961 |
| Top10 | 10/10 | 2025-01-03 to 2026-06-24 | 1.72278834 | 5.28480108 | -0.18210833 | 3.08404887 |
| Top20 | 20/20 | 2025-01-03 to 2026-06-24 | 1.64407907 | 5.30296199 | -0.19955559 | 2.91917850 |
| All | 48/49 | 2025-01-03 to 2026-06-24 | 1.54104357 | 5.30579550 | -0.17982691 | 2.70634281 |

## Interpretation

The supplied basket performed strongly over this 2025-2026 window. The broad 48-stock basket has the best Sharpe in this run, while Top10 has the highest annualized and cumulative return.

This is a historical basket backtest, not a forward model-selected portfolio. It should not be interpreted as a live-trading recommendation without liquidity, risk, and out-of-sample selection checks.

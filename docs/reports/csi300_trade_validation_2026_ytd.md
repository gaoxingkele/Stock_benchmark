# 2026 YTD CSI300 Trading Validation

Strategy: RD-Agent-Quant / DoubleAdapt-family H5 Top30 long-only proxy, equal weight, daily rebalance, 10 bps one-way turnover cost.

## Data Window

- Data was extended with Tushare fragments for 2025-01-01 to 2026-06-21.
- Combined panel: `data/processed/cn_a_share/csi300_2018_2026_ytd/panel.csv`.
- Test rows with valid H5 labels: 2026-01-05 to 2026-06-11, 104 trading days.
- Training: 2018-01-02 to 2023-12-29; validation: 2024-01-02 to 2024-12-31.

## Results

| Variant | Cum Net Return | Annualized Return | Sharpe | MDD | Benchmark Cum Return | Active Cum Return | Avg Turnover | Hit Rate | Max Industry Wt | Size Exposure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| raw | 62.67% | 225.10% | 16.34 | -6.91% | -2.33% | 66.62% | 11.09% | 69.23% | 22.98% | 0.222 |
| industry_size_neutral | 44.57% | 144.28% | 14.68 | -4.94% | -2.33% | 48.07% | 15.29% | 67.31% | 15.06% | 0.099 |

## Interpretation

- 2026 YTD performance is strongly positive. The raw Top30 version returns 62.67% net over the tested window, while the CSI300 equal-weight benchmark proxy is -2.33%.
- The industry/size-neutral version is also strong at 44.57% net, which suggests the result is not only a simple industry or size tilt.
- The annualized returns, 225.10% raw and 144.28% neutralized, are mathematically correct but should not be treated as normal-year expectations because the tested period is only 104 trading days.
- Raw version has higher return but larger industry concentration and size exposure; neutralized version has lower drawdown and lower industry concentration.
- This strengthens the prior conclusion that DoubleAdapt-family is the only current candidate worth deeper trading validation.

## Cautions

1. This is still a proxy implementation, not full official RD-Agent-Quant or DoubleAdapt.
2. The return construction uses overlapping H5 forward returns divided by 5; it is suitable for research screening but must be checked against a real execution simulator.
3. Suspension, limit-up/down, liquidity, slippage, and order fill constraints are still not fully modeled.
4. Because 2026 is partial-year data through mid-June, focus on cumulative return, drawdown, turnover, and consistency rather than annualized return alone.

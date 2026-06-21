# Basic Factor IC Summary

Date: 2026-06-19

Dataset:

```text
data/processed/cn_a_share/csi300_by_date_smoke/panel.csv
```

Window:

```text
2024-01-02 to 2024-01-10
```

Universe:

```text
CSI300 by index_weight union, 300 symbols
```

Output:

```text
factor_lab/validation/basic_factor_ic_csi300_by_date.csv
```

Top factors by absolute RankIC in this short smoke run:

| Factor | IC | RankIC | Notes |
| --- | ---: | ---: | --- |
| `pe` | -0.08336811 | -0.29081431 | Valuation signal; no neutralization yet. |
| `intraday_ret` | 0.25759608 | 0.28726819 | Same-day intraday return. |
| `pb` | -0.16243899 | -0.24725894 | Valuation signal; no neutralization yet. |
| `ret_1` | 0.22730816 | 0.24704159 | 1-day momentum. |
| `close_to_high` | 0.13028983 | 0.21215360 | Position within daily range. |

Interpretation caution:

- This is a 7-trading-day smoke run, so it only validates mechanics.
- The IC values are not statistically meaningful yet.
- Formal factor validation requires a multi-year window, industry/size controls, turnover, decay, and transaction-cost-aware portfolio tests.


# Basic Factor Library

Date: 2026-06-19

Implemented in:

```text
scripts/generate_basic_factors.py
```

## Factors

| Factor | Definition |
| --- | --- |
| `ret_1` | 1-day close-to-close return. |
| `ret_3` | 3-day close-to-close return. |
| `intraday_ret` | close / open - 1. |
| `overnight_ret` | open / pre_close - 1. |
| `high_low_spread` | high / low - 1. |
| `close_to_high` | close / high. |
| `close_to_low` | close / low. |
| `volume_ratio_3` | volume / 3-day rolling average volume. |
| `amount_ratio_3` | amount / 3-day rolling average amount. |
| `turnover_rate` | Tushare daily_basic turnover rate. |
| `volume_ratio` | Tushare daily_basic volume ratio. |
| `pe` | Tushare daily_basic PE. |
| `pb` | Tushare daily_basic PB. |
| `size_log_total_mv` | log(total market value). |
| `size_log_circ_mv` | log(circulating market value). |

## Notes

- These are smoke-test factors, not a complete alpha library.
- Industry/size neutralization is available in `scripts/neutralize_factors.py`.
- Turnover, decay, and stability smoke reports are available in `scripts/evaluate_factor_stability.py`.

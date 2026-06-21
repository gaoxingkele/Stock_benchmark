# Smoke Results Summary

Generated table:

```text
experiments/summary/smoke_results.csv
```

Command:

```bash
python Stock_benchmark/scripts/summarize_smoke_results.py
```

Current included runs:

| Run | Type | Selection | N | Dates | IC | RankIC | ICIR | RankICIR |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm_panel_h1 | model | SUMMARY | 572 |  | 0.02623058 | 0.05295324 | 0.26715893 | 1.88916703 |
| basic_factor_best_raw_h1 | factor | pe | 1716 | 6 | -0.08336811 | -0.29081431 | -2.05819488 | -2.36692384 |
| basic_factor_best_ind_size_neutralized_h1 | factor | pe_ind_size_neu | 1716 | 6 | 0.01350295 | 0.11556740 | 0.47168536 | 1.47941389 |

These are smoke results only. The date range is too short for formal benchmark claims.

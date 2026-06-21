# Factor Stability Smoke Report

Generated outputs:

```text
factor_lab/validation/basic_factor_decay_csi300_by_date.csv
factor_lab/validation/basic_factor_turnover_csi300_by_date.csv
factor_lab/validation/basic_factor_decay_csi300_by_date_neutralized.csv
factor_lab/validation/basic_factor_turnover_csi300_by_date_neutralized.csv
experiments/summary/factor_stability_smoke.csv
```

Commands:

```bash
python Stock_benchmark/scripts/evaluate_factor_stability.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --factors Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke.csv \
  --horizons 1,2,3,5 \
  --top-frac 0.2 \
  --decay-out Stock_benchmark/factor_lab/validation/basic_factor_decay_csi300_by_date.csv \
  --turnover-out Stock_benchmark/factor_lab/validation/basic_factor_turnover_csi300_by_date.csv
```

```bash
python Stock_benchmark/scripts/evaluate_factor_stability.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --factors Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke_neutralized.csv \
  --horizons 1,2,3,5 \
  --top-frac 0.2 \
  --decay-out Stock_benchmark/factor_lab/validation/basic_factor_decay_csi300_by_date_neutralized.csv \
  --turnover-out Stock_benchmark/factor_lab/validation/basic_factor_turnover_csi300_by_date_neutralized.csv
```

## Summary

| Group | Metric | Factor | Value | N | Dates | Extra |
| --- | --- | --- | ---: | ---: | ---: | --- |
| raw | best_abs_rankic_h1 | pe | -0.29081431 | 1716 | 6 | rankicir=-2.36692384 |
| neutralized | best_abs_rankic_h1 | pe_ind_size_neu | 0.11556740 | 1716 | 6 | rankicir=1.47941389 |
| raw | best_abs_rankic_h5 | pe | -0.50912748 | 572 | 2 | rankicir=-9.80241329 |
| neutralized | best_abs_rankic_h5 | pe_ind_size_neu | 0.21418563 | 572 | 2 | rankicir=28.77411561 |
| raw | lowest_top20_turnover | size_log_circ_mv | 0.00833333 | 60.00 | 7 | turnover_obs=6 |
| neutralized | lowest_top20_turnover | pb_ind_size_neu | 0.00555556 | 60.00 | 7 | turnover_obs=6 |

## Limits

The smoke sample covers only 7 trading dates, so H5 ICIR and turnover are used to validate the evaluation path, not to make statistical claims.

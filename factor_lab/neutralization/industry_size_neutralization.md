# Industry And Size Neutralization

This note records the first neutralized alpha validation path on the CSI300 by-date smoke dataset.

## Method

Input factors:

```text
data/features/basic_factors/csi300_by_date_smoke.csv
```

Industry mapping:

```text
data/raw/tushare/csi300_by_date_smoke/stock_basic.csv
```

For each trade date and each factor:

1. Join each symbol to its Tushare `industry`.
2. Subtract the same-date industry mean from the factor.
3. Regress the industry-demeaned factor on `size_log_total_mv`.
4. Save the residual as `<factor>_ind_size_neu`.

`size_log_total_mv` is used as the size control and is not itself emitted as a neutralized factor.

## Commands

```bash
python Stock_benchmark/scripts/neutralize_factors.py \
  --factors Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke.csv \
  --stock-basic Stock_benchmark/data/raw/tushare/csi300_by_date_smoke/stock_basic.csv \
  --out Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke_neutralized.csv
```

```bash
python Stock_benchmark/scripts/evaluate_factor_table.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --factors Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke_neutralized.csv \
  --horizon 1 \
  --out Stock_benchmark/factor_lab/validation/basic_factor_ic_csi300_by_date_neutralized.csv
```

## Current Smoke Output

```text
data/features/basic_factors/csi300_by_date_smoke_neutralized.csv
factor_lab/validation/basic_factor_ic_csi300_by_date_neutralized.csv
```

The smoke run covers 300 CSI300 symbols, 2100 factor rows, and 14 neutralized factors.

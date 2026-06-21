# Factor Lab

Shared alpha factor research code.

```text
factor_lab/
  factor_library/       Reusable factor definitions.
  mining/               Factor discovery/mining algorithms.
  validation/           IC, RankIC, turnover, decay, and stability tests.
  neutralization/       Industry/size/risk neutralization utilities.
```

## Current Runnable Baseline

The first factor pipeline is available on the CSI300 by-date smoke dataset.

Generate factors:

```bash
python Stock_benchmark/scripts/generate_basic_factors.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --out Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke.csv
```

Evaluate factors:

```bash
python Stock_benchmark/scripts/evaluate_factor_table.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --factors Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke.csv \
  --horizon 1 \
  --out Stock_benchmark/factor_lab/validation/basic_factor_ic_csi300_by_date.csv
```

Verified output:

```text
data/features/basic_factors/csi300_by_date_smoke.csv
factor_lab/validation/basic_factor_ic_csi300_by_date.csv
```

The smoke run generates 15 basic price-volume/valuation factors over 300 CSI300 symbols.

Neutralize factors by industry and total market capitalization:

```bash
python Stock_benchmark/scripts/neutralize_factors.py \
  --factors Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke.csv \
  --stock-basic Stock_benchmark/data/raw/tushare/csi300_by_date_smoke/stock_basic.csv \
  --out Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke_neutralized.csv
```

Evaluate neutralized factors:

```bash
python Stock_benchmark/scripts/evaluate_factor_table.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --factors Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke_neutralized.csv \
  --horizon 1 \
  --out Stock_benchmark/factor_lab/validation/basic_factor_ic_csi300_by_date_neutralized.csv
```

Current neutralized result:

```text
data/features/basic_factors/csi300_by_date_smoke_neutralized.csv
factor_lab/validation/basic_factor_ic_csi300_by_date_neutralized.csv
factor_lab/validation/basic_factor_ic_csi300_by_date_neutralized_summary.md
```

Evaluate factor decay and top-quantile turnover:

```bash
python Stock_benchmark/scripts/evaluate_factor_stability.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_by_date_smoke/panel.csv \
  --factors Stock_benchmark/data/features/basic_factors/csi300_by_date_smoke.csv \
  --horizons 1,2,3,5 \
  --top-frac 0.2
```

Current stability report:

```text
docs/reports/factor_stability_smoke.md
experiments/summary/factor_stability_smoke.csv
```

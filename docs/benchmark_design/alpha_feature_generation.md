# Alpha Feature Generation

This benchmark now includes deterministic Alpha158/Alpha360-compatible feature
CSV files for the formal CSI300 2018-2024 dataset.

## Runtime Constraint

The local Qlib runtime cannot currently import the compiled
`qlib.data._libs.rolling` extension. Because of that, Qlib's native expression
handlers cannot be executed in this environment yet.

The current implementation uses:

```text
scripts/generate_alpha_features.py
```

It emits the benchmark-compatible factor table contract:

```text
date,symbol,ts_code,<numeric factor columns...>
```

These files are suitable for the repository's shared IC/RankIC validation and
for first-run model/factor experiments. They are not byte-identical Qlib
Alpha158/Alpha360 handler outputs.

## Generated Artifacts

| Kind | Path | Rows | Features |
| --- | --- | ---: | ---: |
| Alpha158 compatible | `data/features/alpha158/csi300_2018_2024.csv` | 514449 | 80 |
| Alpha360 compatible | `data/features/alpha360/csi300_2018_2024.csv` | 514449 | 286 |

Both paths are recorded in:

```text
configs/datasets/csi300_2018_2024_tushare.json
```

## Validation

H1 factor IC validation was run with:

```bash
python Stock_benchmark/scripts/evaluate_factor_table.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_2018_2024/panel.csv \
  --factors Stock_benchmark/data/features/alpha158/csi300_2018_2024.csv \
  --horizon 1 \
  --out Stock_benchmark/factor_lab/validation/alpha158_ic_csi300_2018_2024_h1.csv

python Stock_benchmark/scripts/evaluate_factor_table.py \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_2018_2024/panel.csv \
  --factors Stock_benchmark/data/features/alpha360/csi300_2018_2024.csv \
  --horizon 1 \
  --out Stock_benchmark/factor_lab/validation/alpha360_ic_csi300_2018_2024_h1.csv
```

Best H1 RankIC rows:

| Feature Set | Factor | N | Dates | IC | RankIC | ICIR | RankICIR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Alpha158 compatible | `klow` | 514121 | 1698 | -0.02513934 | -0.03910449 | -0.16814491 | -0.27476966 |
| Alpha360 compatible | `klow` | 514121 | 1698 | -0.02513934 | -0.03910449 | -0.16814491 | -0.27476966 |

The same best-factor rows are included in:

```text
experiments/summary/smoke_results.csv
```

## Next Step

When Qlib can be imported with compiled rolling operators, run native
`Alpha158` and `Alpha360` handlers against the same CSI300 provider and compare
feature coverage, missingness, and IC rankings against these compatible files.

# CSI300 By-Date Smoke LightGBM H1

Config:

```text
configs/experiments/csi300_by_date_smoke_lightgbm.json
```

Command:

```bash
python Stock_benchmark/scripts/run_lightgbm_smoke.py \
  --config Stock_benchmark/configs/experiments/csi300_by_date_smoke_lightgbm.json
```

Dataset:

```text
data/processed/cn_a_share/csi300_by_date_smoke/panel.csv
```

## Result

| Date | N | IC | RankIC |
| --- | ---: | ---: | ---: |
| 2024-01-08 | 286 | -0.07195286 | 0.02492330 |
| 2024-01-09 | 286 | 0.12441403 | 0.08098319 |
| SUMMARY | 572 | 0.02623058 | 0.05295324 |

Summary ICIR: 0.26715893  
Summary RankICIR: 1.88916703

## Status

This is a smoke test for the shared data-to-metrics loop. It is not yet a formal benchmark result because the date range is intentionally short.

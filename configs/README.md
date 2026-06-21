# Configs

Shared JSON configs for datasets, models, benchmark protocols, and experiment runs.

```text
configs/
  datasets/          Tushare/raw/processed dataset profiles.
  experiments/       Runnable experiment definitions.
  qlib/              Qlib workflow configs.
  splits/            Reusable train/valid/test windows.
  universes/         Reusable stock universe definitions.
```

Validate configs with:

```bash
python Stock_benchmark/scripts/validate_benchmark_config.py Stock_benchmark/configs/experiments/csi300_by_date_smoke_lightgbm.json
```

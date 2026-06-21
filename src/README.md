# Shared Source

Shared benchmark code used by paper-specific implementations.

```text
src/
  data/          Dataset loading, calendar handling, universe filtering.
  labels/        Return, direction, ranking, and risk-adjusted labels.
  features/      Shared feature builders.
  models/        Common baseline model wrappers.
  evaluation/    Metrics, backtests, ranking evaluation, statistical tests.
  utils/         Logging, config, IO, reproducibility helpers.
```


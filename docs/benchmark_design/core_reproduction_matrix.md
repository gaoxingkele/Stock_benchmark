# Core Reproduction Matrix

Date: 2026-06-19

## Current Core Models

| Model | Paper project | Code source | Data requirement | Label setup | First runnable target | Current blocker |
| --- | --- | --- | --- | --- | --- | --- |
| LightGBM baseline | `experiments/baselines` | Local smoke script; later Qlib | CSI300 panel | 1-day then 5-day return | Already ran smoke | Formal Qlib workflow blocked by pyqlib compile |
| TRA | `paper_projects/2021_tra_lin` | `microsoft__qlib/examples/benchmarks/TRA` | Qlib Alpha158/360, sequence data | Rank label, monthly or 5-day | Qlib TRA Alpha360 config | Full Qlib runtime |
| MASTER | `paper_projects/2024_master_li` | `SJTU-DMTai__qlib/examples/benchmarks/MASTER` | Stock handler + market handler | 5-day return with CSRankNorm | MASTER Alpha158 config | Fork-specific Qlib + PyTorch + market features |
| DoubleAdapt | `paper_projects/2023_doubleadapt_zhao` | `SJTU-DMTai__qlib/examples/benchmarks_dynamic/incremental` | Long rolling CSI300 dataset | Trend label; rank optional | GRU + DoubleAdapt run_all | Full Qlib, PyTorch, higher, long incremental split |
| TCTS | `paper_projects/2021_tcts_wu` | `microsoft__qlib/examples/benchmarks/TCTS` | Qlib Alpha360 | multi-horizon labels | TCTS Alpha360 config | Full Qlib runtime and long-history data |

## Execution Order

1. Build full CSI300 Tushare dataset for at least 2018-2024.
2. Convert it to Qlib bin.
3. Fix Qlib runtime by installing MSVC Build Tools or moving to Python 3.10/3.11/WSL.
4. Run formal Qlib LightGBM.
5. Run Transformer/ALSTM baseline.
6. Run TRA.
7. Run MASTER.
8. Define rolling/incremental split and run DoubleAdapt.
9. Run TCTS after Transformer/TRA on the same long-history CSI300 provider.

## Shared Output Contract

Each model run should write:

```text
experiments/paper_runs/<paper_id>/<run_id>/config.yaml
experiments/paper_runs/<paper_id>/<run_id>/metrics.csv
experiments/paper_runs/<paper_id>/<run_id>/predictions.parquet or predictions.csv
experiments/paper_runs/<paper_id>/<run_id>/run_notes.md
```

Required metrics:

- IC
- ICIR
- RankIC
- RankICIR
- annualized return
- information ratio
- max drawdown
- turnover

## China A-Share Smoke Configs

Each core paper now has a machine-readable smoke reproduction config:

```text
paper_projects/2021_tra_lin/configs/china_a_share_smoke.json
paper_projects/2024_master_li/configs/china_a_share_smoke.json
paper_projects/2023_doubleadapt_zhao/configs/china_a_share_smoke.json
paper_projects/2021_tcts_wu/configs/china_a_share_smoke.json
```

Validate them with:

```bash
python Stock_benchmark/scripts/validate_paper_smoke_configs.py
```

These configs point to the shared CSI300 smoke universe, split, H1/H5 labels, Qlib provider directory, and each model's upstream repository entrypoint. They are smoke-stage configs, not formal benchmark results.

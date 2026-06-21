# Paper Model First Runs

This document records the first runnable paper-model experiments on the formal
China A-share CSI300 2018-2024 dataset.

## Scope

The current runtime does not have PyTorch, sklearn, or a working compiled Qlib
runtime. The first runs therefore use `scripts/run_paper_model_baseline.py`,
a NumPy-only implementation of the central mechanism needed to exercise each
paper inside the shared benchmark protocol:

| Paper project | Runnable proxy mechanism |
| --- | --- |
| TRA | Volatility-routed multi-expert ridge sequence model |
| MASTER | Sequence model with cross-sectional market context features |
| DoubleAdapt | Base sequence model plus online symbol-level residual adaptation |
| TCTS | Multi-horizon task models combined by validation-error scheduling |

These results are first runnable benchmark anchors, not official reproduction
numbers. Official/fork implementations remain the next step once the Qlib and
PyTorch runtime is available.

## Dataset And Split

| Field | Value |
| --- | --- |
| Dataset | `csi300_2018_2024` |
| Panel | `data/processed/cn_a_share/csi300_2018_2024/panel.csv` |
| Train | 2018-01-02 to 2021-12-31 |
| Valid | 2022-01-04 to 2022-12-30 |
| Test | 2023-01-03 to 2024-12-31 |
| Lookback | 20 trading days |
| Max train rows | 50,000 sampled rows |
| Features | 16 adjusted Tushare/Qlib numeric fields |

## Commands

Example command shape:

```bash
python Stock_benchmark/scripts/run_paper_model_baseline.py \
  --model tra \
  --panel Stock_benchmark/data/processed/cn_a_share/csi300_2018_2024/panel.csv \
  --horizon 1 \
  --lookback 20 \
  --max-train-rows 50000 \
  --out Stock_benchmark/experiments/paper_runs/tra_formal_csi300_2018_2024_h1.csv
```

Valid `--model` values are `tra`, `master`, `doubleadapt`, and `tcts`.

## Results

| Run | N | IC | RankIC | ICIR | RankICIR |
| --- | ---: | ---: | ---: | ---: | ---: |
| TRA H1 | 150318 | -0.00552884 | -0.02132450 | -0.04673762 | -0.16414648 |
| TRA H5 | 149030 | -0.01290636 | -0.03135955 | -0.10014150 | -0.21385790 |
| MASTER H1 | 150318 | -0.00173863 | -0.01482999 | -0.01296457 | -0.10273796 |
| MASTER H5 | 149030 | -0.01162947 | -0.01968499 | -0.09659950 | -0.14243039 |
| DoubleAdapt H1 | 150318 | 0.00236500 | -0.00312869 | 0.01079150 | -0.01369606 |
| DoubleAdapt H5 | 149030 | 0.06613830 | 0.05671244 | 0.29597755 | 0.25244259 |
| TCTS H1 | 149030 | -0.00719981 | -0.01291857 | -0.05846215 | -0.09407135 |
| TCTS H5 | 149030 | -0.00876161 | -0.01981910 | -0.09463077 | -0.18960886 |

The same rows are appended to:

```text
experiments/summary/smoke_results.csv
```

## Next Reproduction Steps

1. Create PyTorch modules matching TRA, MASTER, DoubleAdapt, and TCTS more
   closely after a stable Python environment is selected.
2. Replace sampled ridge training with full train/valid early-stopped neural
   training.
3. Run official Qlib/fork workflows once `qlib.data._libs.rolling` can be built
   or a compatible Python environment is provisioned.
4. Add per-paper reproduction summaries comparing official assumptions against
   this benchmark's China A-share protocol.

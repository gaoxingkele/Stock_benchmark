# Experiments

## E01: Source availability check
- **Verifies**: C01
- **Setup**:
  - Model: n/a
  - Hardware: local filesystem
  - Dataset: downloaded paper corpus
  - System: `Stock_benchmark/papers`
- **Procedure**:
  1. Read `paper_registry.csv`.
  2. Read `pdf_download_status.csv`.
  3. Confirm PDF and extracted text paths.
- **Metrics**: presence, byte count, PDF header validity
- **Expected outcome**:
  - Registry and PDF evidence exist.
- **Baselines**: none
- **Dependencies**: none

## E02: Engineering traceability check
- **Verifies**: C02
- **Setup**:
  - Model: n/a
  - Hardware: local filesystem
  - Dataset: paper project files and extracted text
  - System: `Stock_benchmark/paper_projects/2021_adarnn_du`
- **Procedure**:
  1. Inspect project notes, repository analysis, reproduction plan, and configs if present.
  2. Bind available materials into `src/` and `evidence/source/`.
- **Metrics**: project files present, config files present
- **Expected outcome**:
  - Available engineering context is linked without inventing missing code.
- **Baselines**: none
- **Dependencies**: E01

## E03: Independent local model verification
- **Verifies**: C03
- **Setup**:
  - Model: adarnn
  - Hardware: local CPU/NumPy or configured runtime
  - Dataset: CSI300 2018-2024 formal benchmark when available
  - System: `experiments/paper_runs`
- **Procedure**:
  1. Match `smoke_results.csv` rows to this paper's model prefix.
  2. Confirm each row's source file exists.
  3. Record IC/RankIC summaries in `evidence/runs/`.
- **Metrics**: IC, RankIC, ICIR, RankICIR, row count
- **Expected outcome**:
  - Source-backed local run rows exist for independently verified papers.
- **Baselines**: LightGBM and Qlib baseline rows in `smoke_results.csv`
- **Dependencies**: E01, E02

## Local run bindings
  - adarnn_formal_h1: `experiments\paper_runs\adarnn_formal_csi300_2018_2024_h1.csv` with IC `-0.01077460` and RankIC `-0.02718109`
  - adarnn_formal_h5: `experiments\paper_runs\adarnn_formal_csi300_2018_2024_h5.csv` with IC `-0.02084717` and RankIC `-0.04531338`

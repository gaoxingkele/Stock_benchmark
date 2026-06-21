# Claims

## C01: Paper is in corpus scope
- **Statement**: `2022_hist_xu` is a valid local corpus paper for `stock trend forecasting`.
- **Status**: supported
- **Falsification criteria**: Remove the paper from `paper_registry.csv` or show the PDF status is invalid.
- **Proof**: [E01]
- **Evidence basis**: The registry row and PDF verification row both exist locally.
- **Interpretation**: The paper can be represented as an ARA artifact.
- **Dependencies**: none
- **Tags**: corpus, pdf

## C02: Local reproduction engineering is represented
- **Statement**: Local project and/or source evidence has been bound into this ARA for `2022_hist_xu`.
- **Status**: hypothesis
- **Falsification criteria**: Show that no local project files, extracted paper text, or registry evidence are linked in the evidence layer.
- **Proof**: [E02]
- **Evidence basis**: Project files present: Not specified in provided sources.
- **Interpretation**: This claim covers engineering traceability, not model performance.
- **Dependencies**: C01
- **Tags**: engineering, project

## C03: Independent local model verification
- **Statement**: `2022_hist_xu` independent local verification status is `complete`.
- **Status**: supported
- **Falsification criteria**: Re-run summary aggregation and find a contradictory source-backed paper-model result status.
- **Proof**: [E03]
- **Evidence basis**: Matching run rows: 2.
- **Interpretation**: `complete` means source-backed local result files exist; it does not imply official reproduction parity.
- **Dependencies**: C01, C02
- **Tags**: verification, benchmark

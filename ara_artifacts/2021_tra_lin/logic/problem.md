# Problem Specification

## Observations

### O1: Registry inclusion
- **Statement**: `2021_tra_lin` is listed in the local paper registry with status `candidate_verified`.
- **Evidence**: `papers/metadata/paper_registry.csv`
- **Implication**: The paper is in scope for the benchmark corpus.

### O2: Local PDF availability
- **Statement**: A local PDF exists with `valid_pdf_header=True` and `3331462` bytes.
- **Evidence**: `papers/metadata/pdf_download_status.csv`
- **Implication**: The paper can be processed without relying on the network.

### O3: Independent verification status
- **Statement**: `complete`.
- **Evidence**: `experiments/summary/smoke_results.csv`
- **Implication**: Completion requires paper-specific local result files for this artifact.

## Gaps

### G1: Full official reproduction
- **Statement**: This ARA records local benchmark evidence, not a complete official-paper reproduction unless stated by run evidence.
- **Caused by**: O3
- **Existing attempts**: Existing `paper_projects/` plans and `experiments/paper_runs/` outputs.
- **Why they fail**: Missing local paper-model outputs for this paper when `independent_verification` is not complete.

## Key Insight
- **Insight**: Treat each paper as an independently verifiable artifact: PDF evidence, local project evidence, config evidence, and run evidence must be bound separately.
- **Derived from**: O1, O2, O3
- **Enables**: Per-paper ARA validation and explicit missing-evidence reporting.

## Assumptions
- A1: Local files under `Stock_benchmark` are the authoritative state for this benchmark.
- A2: Summary rows count as verification evidence only when their source files exist.

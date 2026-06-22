# Problem Specification

## Observations

### O1: Paper belongs to the 31-paper benchmark pool
- **Statement**: `2022_alsp_tf_wang` is included through `paper_24_matrix`.
- **Evidence**: `papers/metadata/paper_target_24.csv`, `experiments/summary/paper_24_comparison_matrix.csv`
- **Implication**: The paper requires an ARA package to satisfy the 31-paper engineering goal.

### O2: Local validation evidence exists
- **Statement**: Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`.
- **Evidence**: `evidence/runs/local_validation.md`
- **Implication**: The artifact can make validation claims without relying on memory or prose-only summaries.

### O3: Source completeness varies by paper
- **Statement**: PDF valid header is `True` and extracted text availability is `True`.
- **Evidence**: `papers/metadata/pdf_download_status.csv`, `papers/extracted/2022_alsp_tf_wang.txt`
- **Implication**: Some method details remain bounded by repository evidence rather than full official reproduction.

## Gaps

### G1: ARA package missing before this compilation
- **Statement**: `2022_alsp_tf_wang` did not have a complete ARA directory before this generated package.
- **Caused by**: O1
- **Existing attempts**: Paper matrices, reports, and validation CSVs existed separately.
- **Why they fail**: They were not linked through ARA claims, experiments, trace, and evidence layers.

## Key Insight
- **Insight**: A paper can be made agent-navigable by binding local validation rows, source metadata, and limitations into a structured ARA even when official reproduction parity is not yet claimed.
- **Derived from**: O1, O2, O3
- **Enables**: Requirement-by-requirement completion checks across the 31-paper pool.

## Assumptions
- A1: The current repository state is authoritative for local validation.
- A2: Generated ARA content must not invent official-code details absent from local evidence.

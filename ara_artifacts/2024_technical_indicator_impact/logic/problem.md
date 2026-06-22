# Problem Specification

## Observations

### O1: Paper belongs to the 31-paper benchmark pool
- **Statement**: `2024_technical_indicator_impact` is included through `expansion_only`.
- **Evidence**: `docs/literature_notes/qlib_talib_arxiv_ccf_expansion.md`, `experiments/unvalidated_candidates/combined_candidate_vs_best_proxy_summary.csv`
- **Implication**: The paper requires an ARA package to satisfy the 31-paper engineering goal.

### O2: Local validation evidence exists
- **Statement**: Runnable proxy validation exists for China A-share, US large-cap, and HK large-cap under the H5 Top30 trading protocol.
- **Evidence**: `evidence/runs/local_validation.md`
- **Implication**: The artifact can make validation claims without relying on memory or prose-only summaries.

### O3: Source completeness varies by paper
- **Statement**: PDF valid header is `False` and extracted text availability is `False`.
- **Evidence**: `papers/metadata/pdf_download_status.csv`, `papers/extracted/2024_technical_indicator_impact.txt`
- **Implication**: Some method details remain bounded by repository evidence rather than full official reproduction.

## Gaps

### G1: ARA package missing before this compilation
- **Statement**: `2024_technical_indicator_impact` did not have a complete ARA directory before this generated package.
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

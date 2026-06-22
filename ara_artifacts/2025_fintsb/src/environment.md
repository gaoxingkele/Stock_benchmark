# Environment

- **Language/runtime**: Python, local repository scripts.
- **Framework**: pandas/csv/NumPy-style local workflows where applicable.
- **Hardware**: local CPU execution; GPU not required for generated ARA compilation.
- **Data sources**: repository CSV summaries, paper metadata, local market panels, and available extracted paper text.
- **Key dependencies**: Python standard library plus project scripts.
- **Protocols**: ARA Level 1 validation; H1/H5 metric matrix or H5 Top30 trading validation depending on paper group.
- **Random seeds**: Not specified in provided sources for ARA generation.

## Source files

- 
`docs/literature_notes/qlib_talib_arxiv_ccf_expansion.md`- `experiments/unvalidated_candidates/combined_candidate_vs_best_proxy_summary.csv`
- `papers/metadata/pdf_download_status.csv`
- `papers/extracted/2025_fintsb.txt` when available

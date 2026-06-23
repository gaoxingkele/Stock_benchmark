# CASE-Lingxi Citation Map

This file maps paper-draft claims to BibTeX keys in `papers/metadata/references.bib`.

| Claim area | Citation keys | Status |
|---|---|---|
| Quant platform / benchmark infrastructure | `yang2020qlib` | added |
| Incremental financial adaptation | `zhao2023doubleadapt` | added |
| Agentic quant research | `li2025rdagentquant`, `tang2025alphaagent` | added |
| Agent RL and self-evolution | `luo2025agentlightning`, `wang2025ragen` | added |
| Time-series SOTA transfer | `nie2023patchtst`, `liu2024itransformer` | added |
| Full 31-method finance registry | `papers/metadata/case_lingxi_citation_coverage.csv` | coverage registry added; 27 pending checks remain |
| Additional SOTA time-series models | pending | add DLinear, Non-stationary Transformer, TimeMixer, FEDformer, foundation models |
| LLM debate / collaborative multi-agent RL | pending | add exact papers after venue/status verification |

## Coverage Files

```text
papers/metadata/references.bib
papers/metadata/case_lingxi_citation_coverage.csv
papers/metadata/references_draft_from_registry.bib
papers/metadata/references_draft_missing_registry.csv
papers/metadata/references_missing_metadata_from_ara.csv
docs/literature/case_lingxi_citation_coverage.md
scripts/validate_case_lingxi_citations.py
scripts/build_case_lingxi_draft_bib.py
scripts/extract_case_lingxi_missing_citation_metadata.py
```

## Source Policy

Venue and author metadata should be checked against primary sources before final submission. Current entries were added from arXiv/ACM/OpenReview-facing metadata and local literature reports.

`references_missing_metadata_from_ara.csv` is not a manuscript bibliography source. It is a reproducible audit aid extracted from existing ARA `PAPER.md` files for 17 rows missing local registry metadata; all 17 currently remain incomplete because author metadata is not verified.

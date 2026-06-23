# CASE-Lingxi Citation Map

This file maps paper-draft claims to BibTeX keys in `papers/metadata/references.bib`.

| Claim area | Citation keys | Status |
|---|---|---|
| Quant platform / benchmark infrastructure | `yang2020qlib` | added |
| Incremental financial adaptation | `zhao2023doubleadapt` | added |
| Agentic quant research | `li2025rdagentquant`, `tang2025alphaagent` | added |
| Agentic alpha generation / evolution | `shi2024alphaforge`, `guo2026alphaprobe`, `liu2025cogalpha` | added |
| Financial routing / graph / transformer baselines | `lin2021tra`, `li2024master`, `xu2022hist`, `xiang2022thgnn`, `huynh2023estimate`, `wu2021tcts`, `duan2022factorvae`, `wang2021hatr`, `wang2022alsptf`, `xia2024cisthpan`, `qian2024mdgnn`, `gao2024diffsformer`, `hu2025finmamba`, `zhu2024lsrigru` | added |
| Time-series adaptation / concept drift | `du2021adarnn`, `li2022ddgda` | added |
| Agent RL and self-evolution | `luo2025agentlightning`, `wang2025ragen`, `wang2021deeptrader`, `wang2019alphastock` | added |
| Time-series SOTA transfer | `zeng2023dlinear`, `liu2022nonstationary`, `nie2023patchtst`, `liu2024itransformer`, `wang2024timemixer`, `zhou2022fedformer`, `hu2025timefilter` | added |
| Time-series foundation models | `ekambaram2024ttm`, `das2024timesfm`, `ansari2024chronos`, `woo2024moirai`, `goswami2024moment` | added |
| Benchmark and technical-indicator references | `wang2025quantbench`, `hu2025fintsb`, `deep2024technicalindicators`, `lu2025tin` | added |
| Ensemble finance reference | `zhang2020doubleensemble` | added |
| Full 31-method finance registry | `papers/metadata/case_lingxi_citation_coverage.csv` | coverage registry added; 0 pending checks remain |
| LLM debate / collaborative multi-agent RL | `du2024multiagentdebate`, `liu2025magrpo` | added |

## Coverage Files

```text
papers/metadata/references.bib
papers/metadata/case_lingxi_citation_coverage.csv
papers/metadata/references_draft_from_registry.bib
papers/metadata/references_draft_missing_registry.csv
papers/metadata/references_missing_metadata_from_ara.csv
docs/literature/case_lingxi_citation_coverage.md
scripts/validate_case_lingxi_citations.py
scripts/validate_references_bib.py
scripts/build_case_lingxi_draft_bib.py
scripts/extract_case_lingxi_missing_citation_metadata.py
```

## Source Policy

Venue and author metadata should be checked against primary sources before final submission. Current entries were added from arXiv, ACM, AAAI, IJCAI, ICML/PMLR, journal, and local literature reports.

`references_missing_metadata_from_ara.csv` is not a manuscript bibliography source. It is a reproducible audit aid extracted from existing ARA `PAPER.md` files for missing local registry metadata; after the 31-method citation pass, it currently contains only the CSV header.

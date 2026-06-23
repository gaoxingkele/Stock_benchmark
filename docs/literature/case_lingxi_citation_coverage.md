# CASE-Lingxi Citation Coverage

Date: 2026-06-23

This report tracks manuscript citation coverage for the 31-method finance registry.

## Files

```text
papers/metadata/references.bib
papers/metadata/case_lingxi_citation_coverage.csv
paper/citation_map.md
scripts/validate_case_lingxi_citations.py
scripts/build_case_lingxi_draft_bib.py
scripts/extract_case_lingxi_missing_citation_metadata.py
papers/metadata/references_draft_from_registry.bib
papers/metadata/references_draft_missing_registry.csv
papers/metadata/references_missing_metadata_from_ara.csv
```

## Current Coverage

| Set | Count |
|---|---:|
| Finance methods in registry | 31 |
| BibTeX entries currently added for finance registry | 14 |
| Pending finance-method citation checks | 17 |
| Extra non-finance/agent/time-series entries currently added | 4 |
| Draft BibTeX entries generated from local registry | 0 |
| Pending entries missing local registry metadata | 17 |
| Missing-registry rows with ARA metadata patch | 17 |
| ARA metadata patch rows still missing verified authors | 17 |

Validation command:

```powershell
python scripts\validate_case_lingxi_citations.py
```

Current validation result:

```text
registry_rows=31
coverage_rows=31
bib_keys=18
coverage_added=14
coverage_pending=17
VALIDATION_PASS
```

Draft generation command:

```powershell
python scripts\build_case_lingxi_draft_bib.py
```

Current draft result:

```text
draft_bib=papers/metadata/references_draft_from_registry.bib entries=0
missing_registry=papers/metadata/references_draft_missing_registry.csv rows=17
```

ARA metadata patch command:

```powershell
python scripts\extract_case_lingxi_missing_citation_metadata.py
```

Current ARA metadata patch result:

```text
metadata_patch=papers/metadata/references_missing_metadata_from_ara.csv rows=17
incomplete_authors=17
```

Added finance-registry keys:

| Paper ID | BibTeX key | Role |
|---|---|---|
| `2020_qlib_yang` | `yang2020qlib` | platform reference |
| `2021_tra_lin` | `lin2021tra` | temporal routing reference |
| `2023_doubleadapt_zhao` | `zhao2023doubleadapt` | adaptation reference |
| `2024_master_li` | `li2024master` | stock transformer reference |
| `2022_hist_xu` | `xu2022hist` | graph stock forecasting reference |
| `2022_thgnn_xiang` | `xiang2022thgnn` | temporal heterogeneous graph reference |
| `2023_estimate_huynh` | `huynh2023estimate` | hypergraph stock movement reference |
| `2024_alphaforge_shi` | `shi2024alphaforge` | agentic alpha-mining reference |
| `2026_alphaprobe_guo` | `guo2026alphaprobe` | agentic alpha-mining reference |
| `2021_adarnn_du` | `du2021adarnn` | time-series adaptation reference |
| `2022_ddg_da_li` | `li2022ddgda` | concept drift adaptation reference |
| `2021_tcts_wu` | `wu2021tcts` | task scheduling / stock forecasting reference |
| `2025_rd_agent_quant_li` | `li2025rdagentquant` | agentic quant reference |
| `2025_alphaagent_tang` | `tang2025alphaagent` | agentic alpha-mining reference |

Added non-registry or cross-domain keys:

| Key | Role |
|---|---|
| `luo2025agentlightning` | agent RL reference |
| `wang2025ragen` | agent self-evolution reference |
| `nie2023patchtst` | time-series SOTA reference |
| `liu2024itransformer` | time-series SOTA reference |

## Policy

Only verified entries should be used in the manuscript text. Pending registry rows should not be cited with invented author, venue, DOI, or arXiv metadata. The ARA metadata patch is a recovery aid only: it identifies titles, years, venues, and local ARA source files for missing-registry rows, but the current patch has incomplete author metadata for all 17 rows and must not be promoted to `references.bib` without primary-source verification.

## Next Citation Work

1. Use `references_missing_metadata_from_ara.csv` to prioritize primary-source checks for the 17 rows missing local registry metadata.
2. Verify the remaining finance-method references from primary sources.
3. Replace pending rows in `papers/metadata/case_lingxi_citation_coverage.csv` with concrete keys.
4. Add complete citation keys for DLinear, Non-stationary Transformer, TimeMixer, FEDformer, TTM, TimesFM, Chronos, Moirai, and MOMENT if they remain in the final related-work section.

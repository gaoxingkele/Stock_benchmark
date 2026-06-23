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
| BibTeX entries currently added for finance registry | 4 |
| Pending finance-method citation checks | 27 |
| Extra non-finance/agent/time-series entries currently added | 4 |
| Draft BibTeX entries generated from local registry | 10 |
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
bib_keys=8
coverage_added=4
coverage_pending=27
VALIDATION_PASS
```

Draft generation command:

```powershell
python scripts\build_case_lingxi_draft_bib.py
```

Current draft result:

```text
draft_bib=papers/metadata/references_draft_from_registry.bib entries=10
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
| `2023_doubleadapt_zhao` | `zhao2023doubleadapt` | adaptation reference |
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

1. Verify the 10 draft BibTeX entries against primary sources, then promote valid entries to `references.bib`.
2. Use `references_missing_metadata_from_ara.csv` to prioritize primary-source checks for the 17 rows missing local registry metadata.
3. Verify the remaining finance-method references from primary sources.
4. Replace pending rows in `papers/metadata/case_lingxi_citation_coverage.csv` with concrete keys.
5. Add complete citation keys for DLinear, Non-stationary Transformer, TimeMixer, FEDformer, TTM, TimesFM, Chronos, Moirai, and MOMENT if they remain in the final related-work section.

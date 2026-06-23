# CASE-Lingxi Citation Coverage

Date: 2026-06-23

This report tracks manuscript citation coverage for the 31-method finance registry.

## Files

```text
papers/metadata/references.bib
papers/metadata/case_lingxi_citation_coverage.csv
paper/citation_map.md
scripts/validate_case_lingxi_citations.py
scripts/validate_references_bib.py
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
| BibTeX entries currently added for finance registry | 31 |
| Pending finance-method citation checks | 0 |
| Extra non-finance/agent/time-series entries currently added | 4 |
| Draft BibTeX entries generated from local registry | 0 |
| Pending entries missing local registry metadata | 0 |
| Missing-registry rows with ARA metadata patch | 0 |
| ARA metadata patch rows still missing verified authors | 0 |

Validation command:

```powershell
python scripts\validate_case_lingxi_citations.py
```

Current validation result:

```text
registry_rows=31
coverage_rows=31
bib_keys=35
coverage_added=31
coverage_pending=0
VALIDATION_PASS
```

BibTeX hygiene validation command:

```powershell
python scripts\validate_references_bib.py
```

Current BibTeX hygiene validation result:

```text
entries=35
keys=35
REFERENCES_BIB_VALIDATION_PASS
```

Draft generation command:

```powershell
python scripts\build_case_lingxi_draft_bib.py
```

Current draft result:

```text
draft_bib=papers/metadata/references_draft_from_registry.bib entries=0
missing_registry=papers/metadata/references_draft_missing_registry.csv rows=0
```

ARA metadata patch command:

```powershell
python scripts\extract_case_lingxi_missing_citation_metadata.py
```

Current ARA metadata patch result:

```text
metadata_patch=papers/metadata/references_missing_metadata_from_ara.csv rows=0
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
| `2022_factorvae_duan` | `duan2022factorvae` | dynamic factor model reference |
| `2021_hatr_wang` | `wang2021hatr` | temporal-relational stock reference |
| `2022_alsp_tf_wang` | `wang2022alsptf` | long-short pattern transformer reference |
| `2024_ci_sthpan_xia` | `xia2024cisthpan` | hypergraph stock selection reference |
| `2024_mdgnn_li` | `qian2024mdgnn` | dynamic graph stock reference |
| `2021_deeptrader_wang` | `wang2021deeptrader` | RL portfolio reference |
| `2019_alphastock_wang` | `wang2019alphastock` | RL stock selection reference |
| `2020_doubleensemble_zhang` | `zhang2020doubleensemble` | ensemble finance reference |
| `2024_diffsformer_gao` | `gao2024diffsformer` | diffusion stock factor reference |
| `2025_finmamba_hu` | `hu2025finmamba` | Mamba stock movement reference |
| `2024_lsr_igru_zhu` | `zhu2024lsrigru` | improved GRU stock reference |
| `2025_timefilter_hu` | `hu2025timefilter` | time-series SOTA reference |
| `2025_alphaagent_tang` | `tang2025alphaagent` | agentic alpha-mining reference |
| `2025_cogalpha_liu` | `liu2025cogalpha` | agentic alpha-mining reference |
| `2025_quantbench_wang` | `wang2025quantbench` | benchmark reference |
| `2025_fintsb` | `hu2025fintsb` | benchmark reference |
| `2024_technical_indicator_impact` | `deep2024technicalindicators` | technical indicator reference |
| `2025_tin` | `lu2025tin` | technical indicator reference |

Added non-registry or cross-domain keys:

| Key | Role |
|---|---|
| `luo2025agentlightning` | agent RL reference |
| `wang2025ragen` | agent self-evolution reference |
| `nie2023patchtst` | time-series SOTA reference |
| `liu2024itransformer` | time-series SOTA reference |

## Policy

Only verified entries should be used in the manuscript text. All 31 finance-registry rows now have BibTeX keys in `references.bib`. The ARA metadata patch remains a recovery aid only; because there are no pending rows, it currently emits an empty table.

## Next Citation Work

1. Add complete citation keys for DLinear, Non-stationary Transformer, TimeMixer, FEDformer, TTM, TimesFM, Chronos, Moirai, and MOMENT if they remain in the final related-work section.
2. Perform venue-specific bibliography polishing only after a target manuscript template is selected.

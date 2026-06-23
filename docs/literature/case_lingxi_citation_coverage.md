# CASE-Lingxi Citation Coverage

Date: 2026-06-23

This report tracks manuscript citation coverage for the 31-method finance registry.

## Files

```text
papers/metadata/references.bib
papers/metadata/case_lingxi_citation_coverage.csv
paper/citation_map.md
```

## Current Coverage

| Set | Count |
|---|---:|
| Finance methods in registry | 31 |
| BibTeX entries currently added for finance registry | 4 |
| Pending finance-method citation checks | 27 |
| Extra non-finance/agent/time-series entries currently added | 4 |

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

Only verified entries should be used in the manuscript text. Pending registry rows should not be cited with invented author, venue, DOI, or arXiv metadata.

## Next Citation Work

1. Verify the remaining 27 finance-method references from primary sources.
2. Add BibTeX entries to `papers/metadata/references.bib`.
3. Replace pending rows in `papers/metadata/case_lingxi_citation_coverage.csv` with concrete keys.
4. Add complete citation keys for DLinear, Non-stationary Transformer, TimeMixer, FEDformer, TTM, TimesFM, Chronos, Moirai, and MOMENT if they remain in the final related-work section.

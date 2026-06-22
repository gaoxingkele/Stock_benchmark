# 31-Paper ARA Engineering And Experiment Audit

Date: 2026-06-22

Scope:
- 24 papers from `papers/metadata/paper_target_24.csv`.
- 14 Qlib / TA-Lib / alpha-mining expansion candidates from `docs/literature_notes/qlib_talib_arxiv_ccf_expansion.md`.
- 7 papers overlap across the two lists, so the deduplicated audit set has 31 papers.

## Summary

| Check | Count | Interpretation |
|---|---:|---|
| Deduplicated papers | 31 | Current full comparison/research pool |
| Full ARA-engineered artifacts | 31 | `ara_artifacts/<paper_id>/` exists with `PAPER.md`, `logic/`, `src/`, `trace/`, `evidence/`, and local validation evidence |
| Not yet ARA-engineered | 0 | All papers in the deduplicated 31-paper pool now have ARA directories |
| Formal / proxy local experiment validation complete | 31 | 24 papers in the original metric matrix; 7 expansion-only papers now validated through `scripts/run_unvalidated_paper_candidates.py` |
| Not yet locally experiment-validated | 0 | The expansion-only candidates now have China A-share, US large-cap, and HK large-cap proxy runs |
| Full ARA + local experiment validation | 31 | All paper artifacts have local validation evidence bound under `evidence/runs/` |
| Level 1 structural validation | 31 / 31 PASS | Checked with `C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py` |

Important distinction:
- For the original 24-paper matrix, "experiment validation complete" means the paper has structured original-paper metrics plus local China A-share H1/H5 paper-inspired proxy results.
- For the seven expansion-only papers, "experiment validation complete" means the paper has a runnable proxy experiment on China A-share, US large-cap, and HK large-cap under the H5 Top30 trading protocol.
- Neither category means every official implementation has been fully reproduced.
- Cross-market US/HK validation now covers the seven expansion-only candidates through paper-inspired proxies. The earlier US/HK/Crypto validation covers 9 implemented model proxies / 5 method families.

## ARA Criteria Used

A paper is marked `complete` for ARA engineering only if all of the following exist:

- `ara_artifacts/<paper_id>/PAPER.md`
- `logic/claims.md`
- `logic/experiments.md`
- `logic/problem.md`
- `logic/concepts.md`
- `src/environment.md` or equivalent source/environment layer
- `trace/exploration_tree.yaml`
- `evidence/README.md`
- H1/H5 run evidence under `evidence/runs/`

## Per-Paper Audit

| # | Paper ID | Venue/status | ARA engineering | Local experiment validation | Notes |
|---:|---|---|---|---|---|
| 1 | `2021_tra_lin` | KDD 2021 | complete | complete | Full ARA artifact; H1/H5 run evidence present |
| 2 | `2023_doubleadapt_zhao` | KDD 2023 | complete | complete | Full ARA artifact; H1/H5 run evidence present |
| 3 | `2024_master_li` | AAAI 2024 | complete | complete | Full ARA artifact; H1/H5 run evidence present |
| 4 | `2022_hist_xu` | venue unverified | complete | complete | Full ARA artifact; H1/H5 run evidence present |
| 5 | `2022_thgnn_xiang` | CIKM 2022 | complete | complete | Generated ARA package; Level 1 PASS |
| 6 | `2023_estimate_huynh` | WSDM 2023 | complete | complete | Generated ARA package; Level 1 PASS |
| 7 | `2024_alphaforge_shi` | preprint / AAAI claim in code source | complete | complete | Generated ARA package; Level 1 PASS |
| 8 | `2026_alphaprobe_guo` | preprint | complete | complete | Generated ARA package; Level 1 PASS |
| 9 | `2021_adarnn_du` | venue unverified | complete | complete | Full ARA artifact; H1/H5 run evidence present |
| 10 | `2022_ddg_da_li` | venue unverified | complete | complete | Generated ARA package; Level 1 PASS |
| 11 | `2021_tcts_wu` | ICML 2021 | complete | complete | Full ARA artifact; H1/H5 run evidence present |
| 12 | `2025_rd_agent_quant_li` | preprint | complete | complete | Generated ARA package; Level 1 PASS |
| 13 | `2022_factorvae_duan` | AAAI 2022 | complete | complete | Generated ARA package; Level 1 PASS |
| 14 | `2021_hatr_wang` | IJCAI 2021 | complete | complete | Generated ARA package; Level 1 PASS |
| 15 | `2022_alsp_tf_wang` | IJCAI 2022 | complete | complete | Generated ARA package; Level 1 PASS |
| 16 | `2024_ci_sthpan_xia` | AAAI 2024 | complete | complete | Generated ARA package; Level 1 PASS |
| 17 | `2024_mdgnn_li` | AAAI 2024 | complete | complete | Generated ARA package; Level 1 PASS |
| 18 | `2021_deeptrader_wang` | AAAI 2021 | complete | complete | Generated ARA package; Level 1 PASS |
| 19 | `2019_alphastock_wang` | KDD 2019 | complete | complete | Generated ARA package; Level 1 PASS |
| 20 | `2020_doubleensemble_zhang` | ICDM 2020 | complete | complete | Generated ARA package; Level 1 PASS |
| 21 | `2024_diffsformer_gao` | preprint | complete | complete | Generated ARA package; Level 1 PASS |
| 22 | `2025_finmamba_hu` | preprint | complete | complete | Generated ARA package; Level 1 PASS |
| 23 | `2024_lsr_igru_zhu` | CIKM 2024 | complete | complete | Generated ARA package; Level 1 PASS |
| 24 | `2025_timefilter_hu` | ICML 2025 | complete | complete | Generated ARA package; Level 1 PASS |
| 25 | `2020_qlib_yang` | arXiv 2020 | complete | complete | Generated ARA package; Level 1 PASS |
| 26 | `2025_alphaagent_tang` | KDD 2025 / arXiv | complete | complete | Generated ARA package; Level 1 PASS |
| 27 | `2025_cogalpha_liu` | arXiv 2025/2026 | complete | complete | Generated ARA package; Level 1 PASS |
| 28 | `2025_quantbench_wang` | arXiv / OpenReview / FITEE 2026 | complete | complete | Generated ARA package; Level 1 PASS |
| 29 | `2025_fintsb` | arXiv 2025 | complete | complete | Generated ARA package; Level 1 PASS |
| 30 | `2024_technical_indicator_impact` | arXiv 2024 | complete | complete | Generated ARA package; Level 1 PASS |
| 31 | `2025_tin` | arXiv 2025 | complete | complete | Generated ARA package; Level 1 PASS |

## Conclusion

The current repository now has a complete 31-paper ARA benchmark at the Level 1 structural standard.

Current state:
- Strongest manually enriched subset: 6 papers with earlier hand-built/core ARA engineering and local H1/H5 evidence.
- Formal comparison subset: 24 papers with structured original metrics and local China A-share H1/H5 proxy validation.
- Expansion-only subset: 7 papers have runnable proxy validation across China A-share, US large-cap, and HK large-cap, and now have generated ARA packages.
- Generated subset: 25 papers were compiled by `scripts/build_missing_ara_31.py` and pass Level 1 validation.

Recommended next engineering order:

1. Enrich generated ARAs with manually reviewed official-code details for the most important strategy papers.
2. Add figure screenshots/table screenshots where source PDFs are available.
3. Upgrade selected generated ARAs from Level 1 structural completeness to deeper Level 2 semantic rigor reviews.

See `docs/reports/unvalidated_paper_candidate_validation.md` for the new seven-paper validation results.

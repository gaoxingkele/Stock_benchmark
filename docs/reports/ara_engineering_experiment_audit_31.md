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
| Full ARA-engineered artifacts | 6 | `ara_artifacts/<paper_id>/` exists with `PAPER.md`, `logic/`, `src/`, `trace/`, `evidence/`, and formal H1/H5 run evidence |
| Not yet ARA-engineered | 25 | No full ARA directory yet |
| Formal local experiment validation complete | 24 | Present in the 24-paper matrix with China A-share H1/H5 proxy runs |
| Not yet locally experiment-validated | 7 | Expansion-only candidates; no local benchmark run yet |
| Full ARA + local experiment validation | 6 | Current strongest reproducible subset |

Important distinction:
- "Experiment validation complete" here means the paper has been bound to the local China A-share H1/H5 paper-inspired proxy protocol and structured original-paper metrics.
- It does not mean every official implementation has been fully reproduced.
- Cross-market US/HK/Crypto validation currently covers 9 implemented model proxies / 5 method families, not all 31 papers.

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
| 5 | `2022_thgnn_xiang` | CIKM 2022 | missing | complete | In 24-paper matrix; no ARA package yet |
| 6 | `2023_estimate_huynh` | WSDM 2023 | missing | complete | In 24-paper matrix; no ARA package yet |
| 7 | `2024_alphaforge_shi` | preprint / AAAI claim in code source | missing | complete | In 24-paper matrix and expansion list; no ARA package yet |
| 8 | `2026_alphaprobe_guo` | preprint | missing | complete | In 24-paper matrix and expansion list; no ARA package yet |
| 9 | `2021_adarnn_du` | venue unverified | complete | complete | Full ARA artifact; H1/H5 run evidence present |
| 10 | `2022_ddg_da_li` | venue unverified | missing | complete | In 24-paper matrix; no ARA package yet |
| 11 | `2021_tcts_wu` | ICML 2021 | complete | complete | Full ARA artifact; H1/H5 run evidence present |
| 12 | `2025_rd_agent_quant_li` | preprint | missing | complete | In 24-paper matrix and expansion list; no ARA package yet |
| 13 | `2022_factorvae_duan` | AAAI 2022 | missing | complete | In 24-paper matrix; no ARA package yet |
| 14 | `2021_hatr_wang` | IJCAI 2021 | missing | complete | In 24-paper matrix; no ARA package yet |
| 15 | `2022_alsp_tf_wang` | IJCAI 2022 | missing | complete | In 24-paper matrix; no ARA package yet |
| 16 | `2024_ci_sthpan_xia` | AAAI 2024 | missing | complete | In 24-paper matrix; no ARA package yet |
| 17 | `2024_mdgnn_li` | AAAI 2024 | missing | complete | In 24-paper matrix; no ARA package yet |
| 18 | `2021_deeptrader_wang` | AAAI 2021 | missing | complete | In 24-paper matrix; no ARA package yet |
| 19 | `2019_alphastock_wang` | KDD 2019 | missing | complete | In 24-paper matrix; no ARA package yet |
| 20 | `2020_doubleensemble_zhang` | ICDM 2020 | missing | complete | In 24-paper matrix; no ARA package yet |
| 21 | `2024_diffsformer_gao` | preprint | missing | complete | In 24-paper matrix; no ARA package yet |
| 22 | `2025_finmamba_hu` | preprint | missing | complete | In 24-paper matrix; no ARA package yet |
| 23 | `2024_lsr_igru_zhu` | CIKM 2024 | missing | complete | In 24-paper matrix; no ARA package yet |
| 24 | `2025_timefilter_hu` | ICML 2025 | missing | complete | In 24-paper matrix; no ARA package yet |
| 25 | `2020_qlib_yang` | arXiv 2020 | missing | missing | Expansion-only infrastructure paper; should be converted into benchmark/protocol ARA rather than strategy ARA |
| 26 | `2025_alphaagent_tang` | KDD 2025 / arXiv | missing | missing | Expansion-only candidate; requires local factor-operator search implementation |
| 27 | `2025_cogalpha_liu` | arXiv 2025/2026 | missing | missing | Expansion-only candidate; requires code-based factor generation protocol |
| 28 | `2025_quantbench_wang` | arXiv / OpenReview / FITEE 2026 | missing | missing | Expansion-only benchmark paper; should be treated as evaluation-protocol ARA |
| 29 | `2025_fintsb` | arXiv 2025 | missing | missing | Expansion-only benchmark paper; no local financial time-series benchmark binding yet |
| 30 | `2024_technical_indicator_impact` | arXiv 2024 | missing | missing | Expansion-only TA-Lib-style feature paper; no local indicator ablation yet |
| 31 | `2025_tin` | arXiv 2025 | missing | missing | Expansion-only technical-indicator modeling paper; no local model implementation yet |

## Conclusion

The current repository is not yet a full 31-paper ARA benchmark.

Current state:
- Strongest subset: 6 papers with complete ARA engineering and local H1/H5 evidence.
- Formal comparison subset: 24 papers with structured original metrics and local China A-share H1/H5 proxy validation.
- Expansion-only subset: 7 papers that are useful for the next research direction but still need ARA compilation and experiment binding.

Recommended next engineering order:

1. Convert `2025_rd_agent_quant_li`, `2024_alphaforge_shi`, and `2026_alphaprobe_guo` into full ARA artifacts because they are closest to the current best strategy and alpha-mining direction.
2. Convert `2020_qlib_yang` and `2025_quantbench_wang` as protocol/benchmark ARAs, not strategy ARAs.
3. Add TA-Lib-style indicator experiments for `2024_technical_indicator_impact` and `2025_tin`.
4. Only after those bindings exist, call the project a 31-paper ARA-engineered benchmark.

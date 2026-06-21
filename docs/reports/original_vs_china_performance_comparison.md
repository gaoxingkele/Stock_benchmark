# Original Paper vs China A-share Performance Comparison

Source tables: `papers/metadata/original_experiment_results.csv` and `experiments/summary/paper_24_comparison_matrix.csv`.

## Summary

- Target papers compared: 24
- Papers with directly comparable RankIC: 11
- Papers with directly comparable IC: 14
- Papers with only portfolio/classification/forecasting metrics in the original paper: 8
- China A-share results use the local CSI300 2018-2024 H1/H5 paper-inspired proxy runs, not full official model reproductions for every paper.

## RankIC Comparison

- Positive China H5 RankIC delta: 1/11
- Within +/-0.01 of original RankIC: 2/11
- Average H5 RankIC delta: -0.1222

| Paper | Original Best RankIC | China H1 RankIC | China H5 RankIC | H5 Delta |
|---|---:|---:|---:|---:|
| 2025_rd_agent_quant_li | 0.0499 | -0.0031 | 0.0567 | 0.0068 |
| 2023_doubleadapt_zhao | 0.0621 | -0.0031 | 0.0567 | -0.0054 |
| 2024_diffsformer_gao | 0.0672 | -0.0031 | 0.0567 | -0.0105 |
| 2022_factorvae_duan | 0.0550 | -0.0148 | -0.0197 | -0.0747 |
| 2024_alphaforge_shi | 0.0589 | -0.0148 | -0.0197 | -0.0786 |
| 2021_tcts_wu | 0.0750 | -0.0129 | -0.0198 | -0.0948 |
| 2024_master_li | 0.0760 | -0.0148 | -0.0197 | -0.0957 |
| 2026_alphaprobe_guo | 0.1135 | -0.0148 | -0.0197 | -0.1332 |
| 2021_adarnn_du | 0.1100 | -0.0272 | -0.0453 | -0.1553 |
| 2022_hist_xu | 0.1260 | -0.0143 | -0.0303 | -0.1563 |
| 2023_estimate_huynh | 0.5160 | -0.0143 | -0.0303 | -0.5463 |

## IC Comparison

- Positive China H5 IC delta: 2/14
- Within +/-0.01 of original IC: 2/14
- Average H5 IC delta: -0.0705

| Paper | Original Best IC | China H1 IC | China H5 IC | H5 Delta |
|---|---:|---:|---:|---:|
| 2025_rd_agent_quant_li | 0.0532 | 0.0024 | 0.0661 | 0.0129 |
| 2024_diffsformer_gao | 0.0603 | 0.0024 | 0.0661 | 0.0058 |
| 2023_doubleadapt_zhao | 0.0687 | 0.0024 | 0.0661 | -0.0026 |
| 2024_mdgnn_li | 0.0322 | -0.0046 | -0.0163 | -0.0485 |
| 2020_doubleensemble_zhang | 0.1150 | 0.0024 | 0.0661 | -0.0489 |
| 2024_alphaforge_shi | 0.0440 | -0.0017 | -0.0116 | -0.0556 |
| 2024_ci_sthpan_xia | 0.0530 | -0.0046 | -0.0163 | -0.0693 |
| 2021_tra_lin | 0.0590 | -0.0055 | -0.0129 | -0.0719 |
| 2024_master_li | 0.0640 | -0.0017 | -0.0116 | -0.0756 |
| 2023_estimate_huynh | 0.0800 | -0.0046 | -0.0163 | -0.0963 |
| 2026_alphaprobe_guo | 0.0904 | -0.0017 | -0.0116 | -0.1020 |
| 2021_adarnn_du | 0.1150 | -0.0108 | -0.0208 | -0.1358 |
| 2022_hist_xu | 0.1310 | -0.0046 | -0.0163 | -0.1473 |
| 2022_ddg_da_li | 0.1312 | -0.0108 | -0.0208 | -0.1520 |

## Interpretation

- The strongest transferred performance is in the DoubleAdapt-family proxy runs: RD-Agent-Quant, DiffsFormer, DoubleAdapt, and DoubleEnsemble have positive or near-original IC/RankIC on H5.
- Graph/market-structure papers mapped to the HIST-style proxy generally underperform their original reported IC/RankIC on the local A-share protocol.
- Several papers report portfolio, classification, or forecasting metrics rather than IC/RankIC, so their original results are not numerically comparable to RankIC/IC without additional metric-family normalization.
- Negative deltas should be read as protocol-transfer gaps plus proxy-implementation gaps, not as definitive failures of the original papers.

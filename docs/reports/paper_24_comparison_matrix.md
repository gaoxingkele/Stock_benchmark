# 24-Paper Original-vs-China Experiment Matrix

This report is generated from `papers/metadata/paper_target_24.csv`, `papers/metadata/original_experiment_results.csv`, local PDF/extracted-text status, ARA evidence folders, and `experiments/summary/smoke_results.csv`.

## Coverage Summary

- Target papers: 24
- Locally registered papers: 12
- Valid local PDFs: 22
- Extracted text files: 22
- Papers with original table mentions detected: 20
- Papers with structured original metric rows: 24
- Papers with China A-share H1/H5 runs complete: 24
- Papers ready for metric-level comparison: 24
- Papers partially ready for comparison: 0

## Matrix

| Paper | Venue | Original data status | Original best IC | Original best RankIC | China H1 RankIC | China H5 RankIC | H5 RankIC delta | Comparison status |
|---|---|---|---:|---:|---:|---:|---:|---|
| 2021_tra_lin | KDD 2021 | structured_original_metrics_available | 0.05900000 |  | -0.02132450 | -0.03135955 |  | ready_for_metric_level_comparison |
| 2023_doubleadapt_zhao | KDD 2023 | structured_original_metrics_available | 0.06870000 | 0.06210000 | -0.00312869 | 0.05671244 | -0.00538756 | ready_for_metric_level_comparison |
| 2024_master_li | AAAI 2024 | structured_original_metrics_available | 0.06400000 | 0.07600000 | -0.01482999 | -0.01968499 | -0.09568499 | ready_for_metric_level_comparison |
| 2022_hist_xu | venue_unverified | structured_original_metrics_available | 0.13100000 | 0.12600000 | -0.01433130 | -0.03030684 | -0.15630684 | ready_for_metric_level_comparison |
| 2022_thgnn_xiang | CIKM 2022 | structured_original_metrics_available |  |  | -0.01433130 | -0.03030684 |  | ready_for_metric_level_comparison |
| 2023_estimate_huynh | WSDM 2023 | structured_original_metrics_available | 0.08000000 | 0.51600000 | -0.01433130 | -0.03030684 | -0.54630684 | ready_for_metric_level_comparison |
| 2024_alphaforge_shi | preprint | structured_original_metrics_available | 0.04400000 | 0.05890000 | -0.01482999 | -0.01968499 | -0.07858499 | ready_for_metric_level_comparison |
| 2026_alphaprobe_guo | preprint | structured_original_metrics_available | 0.09040000 | 0.11350000 | -0.01482999 | -0.01968499 | -0.13318499 | ready_for_metric_level_comparison |
| 2021_adarnn_du | venue_unverified | structured_original_metrics_available | 0.11500000 | 0.11000000 | -0.02718109 | -0.04531338 | -0.15531338 | ready_for_metric_level_comparison |
| 2022_ddg_da_li | venue_unverified | structured_original_metrics_available | 0.13120000 |  | -0.02718109 | -0.04531338 |  | ready_for_metric_level_comparison |
| 2021_tcts_wu | ICML 2021 | structured_original_metrics_available |  | 0.07500000 | -0.01291857 | -0.01981910 | -0.09481910 | ready_for_metric_level_comparison |
| 2025_rd_agent_quant_li | preprint | structured_original_metrics_available | 0.05320000 | 0.04990000 | -0.00312869 | 0.05671244 | 0.00681244 | ready_for_metric_level_comparison |
| 2022_factorvae_duan | AAAI 2022 | structured_original_metrics_available |  | 0.05500000 | -0.01482999 | -0.01968499 | -0.07468499 | ready_for_metric_level_comparison |
| 2021_hatr_wang | IJCAI 2021 | structured_original_metrics_available |  |  | -0.01433130 | -0.03030684 |  | ready_for_metric_level_comparison |
| 2022_alsp_tf_wang | IJCAI 2022 | structured_original_metrics_available |  |  | -0.02132450 | -0.03135955 |  | ready_for_metric_level_comparison |
| 2024_ci_sthpan_xia | AAAI 2024 | structured_original_metrics_available | 0.05300000 |  | -0.01433130 | -0.03030684 |  | ready_for_metric_level_comparison |
| 2024_mdgnn_li | AAAI 2024 | structured_original_metrics_available | 0.03220000 |  | -0.01433130 | -0.03030684 |  | ready_for_metric_level_comparison |
| 2021_deeptrader_wang | AAAI 2021 | structured_original_metrics_available |  |  | -0.02132450 | -0.03135955 |  | ready_for_metric_level_comparison |
| 2019_alphastock_wang | KDD 2019 | structured_original_metrics_available |  |  | -0.02132450 | -0.03135955 |  | ready_for_metric_level_comparison |
| 2020_doubleensemble_zhang | ICDM 2020 | structured_original_metrics_available | 0.11500000 |  | -0.00312869 | 0.05671244 |  | ready_for_metric_level_comparison |
| 2024_diffsformer_gao | preprint | structured_original_metrics_available | 0.06030000 | 0.06720000 | -0.00312869 | 0.05671244 | -0.01048756 | ready_for_metric_level_comparison |
| 2025_finmamba_hu | preprint | structured_original_metrics_available |  |  | -0.01433130 | -0.03030684 |  | ready_for_metric_level_comparison |
| 2024_lsr_igru_zhu | CIKM 2024 | structured_original_metrics_available |  |  | -0.01433130 | -0.03030684 |  | ready_for_metric_level_comparison |
| 2025_timefilter_hu | ICML 2025 | structured_original_metrics_available |  |  | -0.01291857 | -0.01981910 |  | ready_for_metric_level_comparison |

## Interpretation

- `formal_h1_h5_complete` means the local China A-share CSI300 2018-2024 protocol has both H1 and H5 paper-inspired runs in the summary table.
- `structured_original_metrics_available` means at least one original-paper experiment table has been transcribed into `papers/metadata/original_experiment_results.csv`.
- `table_mentions_extracted_pending_numeric_transcription` means original paper experiment tables were found in extracted text, but the numeric table contents still need manual or stronger PDF-table extraction before final comparison.
- `missing_pdf_text_and_original_result_data` marks the next acquisition queue: download the paper, extract text/tables, then bind official metrics.
- `H5 RankIC delta` is `China A-share H5 RankIC - original best RankIC`; blank values mean the original paper did not report RankIC in the transcribed rows.

## Next Data Work

1. Add metric-family normalization so classification, ranking, portfolio, and alpha-mining papers can be compared without mixing incompatible scores.

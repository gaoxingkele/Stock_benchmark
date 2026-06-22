# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024_diffsformer_gao | formal_h1_h5_complete | -0.00312869 | 0.00236500 | 0.05671244 | 0.06613830 | 0.06030000 | 0.06720000 | -0.01048756 | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024_diffsformer_gao | Table III | CSI300 | DiffsFormer+Transformer | proposed_augmentation | main | RR | 0.3127 | 0.0113 | overall | papers/extracted/2024_diffsformer_gao.txt:819 | verified_from_extracted_text |
| 2024_diffsformer_gao | Table III | CSI300 | DiffsFormer+Transformer | proposed_augmentation | main | IC | 0.0603 | 0.0025 | overall | papers/extracted/2024_diffsformer_gao.txt:819 | verified_from_extracted_text |
| 2024_diffsformer_gao | Table III | CSI300 | DiffsFormer+Transformer | proposed_augmentation | main | RankIC | 0.0672 | 0.0017 | overall | papers/extracted/2024_diffsformer_gao.txt:819 | verified_from_extracted_text |
| 2024_diffsformer_gao | Table IV | CSI800 | DiffsFormer+Transformer | proposed_augmentation | main | RR | 0.1903 | 0.0382 | overall | papers/extracted/2024_diffsformer_gao.txt:831 | verified_from_extracted_text |
| 2024_diffsformer_gao | Table IV | CSI800 | DiffsFormer+Transformer | proposed_augmentation | main | IC | 0.0426 | 0.0018 | overall | papers/extracted/2024_diffsformer_gao.txt:831 | verified_from_extracted_text |
| 2024_diffsformer_gao | Table IV | CSI800 | DiffsFormer+Transformer | proposed_augmentation | main | RankIC | 0.0556 | 0.0022 | overall | papers/extracted/2024_diffsformer_gao.txt:831 | verified_from_extracted_text |

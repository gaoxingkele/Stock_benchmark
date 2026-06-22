# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024_alphaforge_shi | formal_h1_h5_complete | -0.01482999 | -0.00173863 | -0.01968499 | -0.01162947 | 0.04400000 | 0.05890000 | -0.07858499 | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024_alphaforge_shi | Table 1 | CSI300 | Ours | proposed | main | IC | 0.0440 | 0.0056 | overall | papers/extracted/2024_alphaforge_shi.txt:507 | verified_from_extracted_text |
| 2024_alphaforge_shi | Table 1 | CSI300 | Ours | proposed | main | RankIC | 0.0589 | 0.0069 | overall | papers/extracted/2024_alphaforge_shi.txt:507 | verified_from_extracted_text |
| 2024_alphaforge_shi | Table 1 | CSI500 | Ours | proposed | main | IC | 0.0284 | 0.0058 | overall | papers/extracted/2024_alphaforge_shi.txt:507 | verified_from_extracted_text |
| 2024_alphaforge_shi | Table 1 | CSI500 | Ours | proposed | main | RankIC | 0.0557 | 0.0058 | overall | papers/extracted/2024_alphaforge_shi.txt:507 | verified_from_extracted_text |

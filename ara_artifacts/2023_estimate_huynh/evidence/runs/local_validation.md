# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023_estimate_huynh | formal_h1_h5_complete | -0.01433130 | -0.00457830 | -0.03030684 | -0.01629816 | 0.08000000 | 0.51600000 | -0.54630684 | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023_estimate_huynh | Table 3 | Average | ESTIMATE | proposed | phases_average | Return | 0.102 |  | overall | papers/extracted/2023_estimate_huynh.txt:790 | verified_from_extracted_text |
| 2023_estimate_huynh | Table 3 | Average | ESTIMATE | proposed | phases_average | IC | 0.080 |  | overall | papers/extracted/2023_estimate_huynh.txt:790 | verified_from_extracted_text |
| 2023_estimate_huynh | Table 3 | Average | ESTIMATE | proposed | phases_average | RankIC | 0.516 |  | overall | papers/extracted/2023_estimate_huynh.txt:790 | verified_from_extracted_text |
| 2023_estimate_huynh | Table 3 | Average | ESTIMATE | proposed | phases_average | Prec@N | 0.627 |  | overall | papers/extracted/2023_estimate_huynh.txt:790 | verified_from_extracted_text |

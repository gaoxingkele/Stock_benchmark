# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022_alsp_tf_wang | formal_h1_h5_complete | -0.02132450 | -0.00552884 | -0.03135955 | -0.01290636 |  |  |  | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022_alsp_tf_wang | Table 1 | NASDAQ | ALSP-TF | proposed | main | SR | 1.55 |  | portfolio | papers/extracted/2022_alsp_tf_wang.txt:623 | verified_from_extracted_text |
| 2022_alsp_tf_wang | Table 1 | NASDAQ | ALSP-TF | proposed | main | IRR | 0.53 |  | portfolio | papers/extracted/2022_alsp_tf_wang.txt:623 | verified_from_extracted_text |
| 2022_alsp_tf_wang | Table 1 | NYSE | ALSP-TF | proposed | main | SR | 1.24 |  | portfolio | papers/extracted/2022_alsp_tf_wang.txt:623 | verified_from_extracted_text |
| 2022_alsp_tf_wang | Table 1 | NYSE | ALSP-TF | proposed | main | IRR | 0.41 |  | portfolio | papers/extracted/2022_alsp_tf_wang.txt:623 | verified_from_extracted_text |
| 2022_alsp_tf_wang | Table 1 | TSE | ALSP-TF | proposed | main | SR | 1.27 |  | portfolio | papers/extracted/2022_alsp_tf_wang.txt:623 | verified_from_extracted_text |
| 2022_alsp_tf_wang | Table 1 | TSE | ALSP-TF | proposed | main | IRR | 0.71 |  | portfolio | papers/extracted/2022_alsp_tf_wang.txt:623 | verified_from_extracted_text |
